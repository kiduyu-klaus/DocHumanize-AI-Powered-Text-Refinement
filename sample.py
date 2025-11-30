#!/usr/bin/env python3
"""
sample.py - Test script for humanize_with_ollama functions

This script demonstrates both streaming and non-streaming humanization.
"""

import sys
import time
from ollama_humanize import humanize_with_ollama, humanize_with_ollama_streaming


# Sample AI-generated texts to test
SAMPLE_TEXTS = {
    "short": """Artificial intelligence represents a transformative technological paradigm that encompasses 
the development of sophisticated computational systems capable of performing tasks that traditionally 
necessitate human cognitive capabilities.""",
    
    "medium": """The implementation of machine learning algorithms facilitates the optimization of 
predictive analytics across diverse domains. These advanced methodologies leverage statistical 
techniques to identify patterns within large-scale datasets. Consequently, organizations can 
derive actionable insights that enhance decision-making processes and operational efficiency. 
Furthermore, the integration of neural networks has revolutionized the field by enabling 
unprecedented levels of accuracy in classification tasks.""",
    
    "long": """In the contemporary digital landscape, cybersecurity has emerged as a paramount concern 
for organizations worldwide. The proliferation of sophisticated cyber threats necessitates the 
implementation of robust security frameworks. These frameworks encompass multiple layers of defense 
mechanisms: network security protocols, endpoint protection systems, and advanced threat detection 
algorithms. Moreover, the adoption of zero-trust architecture represents a paradigm shift in how 
organizations approach security. This methodology operates on the principle that no entity should 
be trusted by default, regardless of whether it originates from within or outside the network 
perimeter. Consequently, continuous verification and authentication become integral components 
of the security infrastructure."""
}


def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)


def print_header(text):
    """Print a formatted header"""
    print_separator()
    print(f"  {text}")
    print_separator()


def streaming_callback(chunk):
    """Callback function for streaming output"""
    print(chunk, end='', flush=True)


def test_non_streaming(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434"):
    """Test non-streaming humanization"""
    print_header("TEST: Non-Streaming Humanization")
    
    print("\n📝 Original Text:")
    print("-" * 80)
    print(text)
    print("-" * 80)
    
    print("\n⏳ Processing (non-streaming)...\n")
    start_time = time.time()
    
    try:
        humanized = humanize_with_ollama(
            text,
            model=model,
            ollama_url=ollama_url,
            temperature=0.7,
            max_tokens=2000
        )
        
        elapsed_time = time.time() - start_time
        
        print("\n✅ Humanized Text:")
        print("-" * 80)
        print(humanized)
        print("-" * 80)
        print(f"\n⏱️  Processing time: {elapsed_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def test_streaming(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434"):
    """Test streaming humanization"""
    print_header("TEST: Streaming Humanization")
    
    print("\n📝 Original Text:")
    print("-" * 80)
    print(text)
    print("-" * 80)
    
    print("\n⏳ Processing (streaming)...\n")
    print("✅ Humanized Text (live):")
    print("-" * 80)
    
    start_time = time.time()
    
    try:
        humanized = humanize_with_ollama_streaming(
            text,
            model=model,
            ollama_url=ollama_url,
            temperature=0.7,
            max_tokens=2000,
            callback=streaming_callback
        )
        
        elapsed_time = time.time() - start_time
        
        print()
        print("-" * 80)
        print(f"\n⏱️  Processing time: {elapsed_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def test_comparison(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434"):
    """Compare streaming vs non-streaming side by side"""
    print_header("TEST: Streaming vs Non-Streaming Comparison")
    
    print("\n📝 Original Text:")
    print("-" * 80)
    print(text)
    print("-" * 80)
    
    # Non-streaming test
    print("\n⏳ Running non-streaming test...")
    start_time_non = time.time()
    
    try:
        humanized_non = humanize_with_ollama(
            text,
            model=model,
            ollama_url=ollama_url,
            temperature=0.7,
            max_tokens=2000
        )
        time_non = time.time() - start_time_non
        print(f"✅ Non-streaming completed in {time_non:.2f} seconds")
    except Exception as e:
        print(f"❌ Non-streaming failed: {str(e)}")
        humanized_non = None
        time_non = 0
    
    # Streaming test
    print("\n⏳ Running streaming test...")
    start_time_stream = time.time()
    
    try:
        humanized_stream = humanize_with_ollama_streaming(
            text,
            model=model,
            ollama_url=ollama_url,
            temperature=0.7,
            max_tokens=2000
        )
        time_stream = time.time() - start_time_stream
        print(f"✅ Streaming completed in {time_stream:.2f} seconds")
    except Exception as e:
        print(f"❌ Streaming failed: {str(e)}")
        humanized_stream = None
        time_stream = 0
    
    # Display results
    print("\n" + "=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)
    
    if humanized_non:
        print("\n🔹 Non-Streaming Output:")
        print("-" * 80)
        print(humanized_non)
        print("-" * 80)
    
    if humanized_stream:
        print("\n🔹 Streaming Output:")
        print("-" * 80)
        print(humanized_stream)
        print("-" * 80)
    
    print("\n📊 Performance:")
    print(f"   Non-streaming: {time_non:.2f} seconds")
    print(f"   Streaming:     {time_stream:.2f} seconds")
    
    if time_non > 0 and time_stream > 0:
        diff = abs(time_non - time_stream)
        faster = "Streaming" if time_stream < time_non else "Non-streaming"
        print(f"   Difference:    {diff:.2f} seconds ({faster} was faster)")


def main():
    """Main test runner"""
    print_separator("*")
    print("  OLLAMA HUMANIZATION TEST SUITE")
    print_separator("*")
    
    # Configuration
    MODEL = "cogito-2.1:671b-cloud"
    OLLAMA_URL = "http://localhost:11434"
    
    print(f"\n⚙️  Configuration:")
    print(f"   Model: {MODEL}")
    print(f"   URL:   {OLLAMA_URL}")
    
    # Check if custom settings provided via command line
    if len(sys.argv) > 1:
        MODEL = sys.argv[1]
        print(f"   (Model overridden from command line)")
    
    if len(sys.argv) > 2:
        OLLAMA_URL = sys.argv[2]
        print(f"   (URL overridden from command line)")
    
    print()
    
    # Test menu
    while True:
        print_separator("-")
        print("\n📋 TEST MENU:")
        print("   1. Test Non-Streaming (short text)")
        print("   2. Test Streaming (short text)")
        print("   3. Test Non-Streaming (medium text)")
        print("   4. Test Streaming (medium text)")
        print("   5. Test Non-Streaming (long text)")
        print("   6. Test Streaming (long text)")
        print("   7. Compare Streaming vs Non-Streaming (medium text)")
        print("   8. Run all tests")
        print("   9. Exit")
        
        choice = input("\n👉 Select option (1-9): ").strip()
        
        print()
        
        if choice == "1":
            test_non_streaming(SAMPLE_TEXTS["short"], MODEL, OLLAMA_URL)
        elif choice == "2":
            test_streaming(SAMPLE_TEXTS["short"], MODEL, OLLAMA_URL)
        elif choice == "3":
            test_non_streaming(SAMPLE_TEXTS["medium"], MODEL, OLLAMA_URL)
        elif choice == "4":
            test_streaming(SAMPLE_TEXTS["medium"], MODEL, OLLAMA_URL)
        elif choice == "5":
            test_non_streaming(SAMPLE_TEXTS["long"], MODEL, OLLAMA_URL)
        elif choice == "6":
            test_streaming(SAMPLE_TEXTS["long"], MODEL, OLLAMA_URL)
        elif choice == "7":
            test_comparison(SAMPLE_TEXTS["medium"], MODEL, OLLAMA_URL)
        elif choice == "8":
            print_header("RUNNING ALL TESTS")
            test_non_streaming(SAMPLE_TEXTS["short"], MODEL, OLLAMA_URL)
            print("\n")
            test_streaming(SAMPLE_TEXTS["short"], MODEL, OLLAMA_URL)
            print("\n")
            test_comparison(SAMPLE_TEXTS["medium"], MODEL, OLLAMA_URL)
            print("\n")
            print_header("ALL TESTS COMPLETED")
        elif choice == "9":
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1-9.")
        
        print("\n")
        input("Press Enter to continue...")
        print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)