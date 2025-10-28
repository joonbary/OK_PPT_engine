#!/usr/bin/env python3
"""
Test script for Enhanced TextFitter
Tests all major functionality and performance improvements
"""

import time
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.text_fitter import TextFitter


def test_basic_functionality():
    """Test basic TextFitter functionality"""
    print("=" * 60)
    print("Testing Enhanced TextFitter - Basic Functionality")
    print("=" * 60)
    
    fitter = TextFitter()
    
    # Test text samples
    test_texts = [
        "This is a simple English text for testing.",
        "안녕하세요. 이것은 한국어 테스트 텍스트입니다. 맥킨지 PPT 시스템에서 사용됩니다.",
        "Mixed language text: 한국어와 English가 섞인 텍스트입니다. Performance testing 중입니다.",
        "Very long text " * 50,  # Long text for stress testing
        "中文测试文本，用于测试中文字符的处理能力。"
    ]
    
    print(f"[OK] TextFitter initialized successfully")
    print(f"[OK] Available fonts: {len(fitter.available_fonts)}")
    print(f"[OK] Font families: {list(fitter.font_families.keys())}")
    
    # Test text measurement
    for i, text in enumerate(test_texts[:3]):  # Test first 3 texts
        try:
            width, height = fitter.measure_text_precise(text, 14, 'Calibri')
            print(f"[OK] Text {i+1} measurement: {width:.3f}\" x {height:.3f}\"")
        except Exception as e:
            print(f"[ERROR] Text {i+1} measurement failed: {e}")
    
    return fitter


def test_text_fitting():
    """Test enhanced text fitting capabilities"""
    print("\n" + "=" * 60)
    print("Testing Enhanced Text Fitting")
    print("=" * 60)
    
    fitter = TextFitter()
    
    # Test cases
    test_cases = [
        {
            "text": "This is a simple test to see how well the text fits in a box with specific dimensions.",
            "box_width": 4.0,  # inches
            "box_height": 2.0,  # inches
            "name": "Simple English"
        },
        {
            "text": "안녕하세요. 이것은 한국어 텍스트 피팅 테스트입니다. 박스 크기에 맞게 자동으로 조정되는지 확인합니다.",
            "box_width": 3.5,
            "box_height": 1.5,
            "name": "Korean Text"
        },
        {
            "text": "Mixed language text with 한글과 영어가 함께 있는 텍스트입니다. This should test the enhanced algorithms properly.",
            "box_width": 5.0,
            "box_height": 2.5,
            "name": "Mixed Language"
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting: {case['name']}")
        print(f"Text: {case['text'][:50]}...")
        print(f"Box: {case['box_width']}\" x {case['box_height']}\"")
        
        try:
            result = fitter.fit_text_to_box(
                case['text'], 
                case['box_width'], 
                case['box_height'],
                use_binary_search=True
            )
            
            print(f"[OK] Fits: {result['fits']}")
            print(f"[OK] Font size: {result['adjusted_font_size']}pt")
            print(f"[OK] Truncated: {result['truncated']}")
            print(f"[OK] Dimensions: {result['actual_width']:.3f}\" x {result['actual_height']:.3f}\"")
            print(f"[OK] Processing time: {result['processing_time']*1000:.2f}ms")
            print(f"[OK] Method: {result['measurement_method']}")
            
        except Exception as e:
            print(f"[ERROR] Failed: {e}")


def test_smart_truncation():
    """Test intelligent truncation features"""
    print("\n" + "=" * 60)
    print("Testing Smart Truncation")
    print("=" * 60)
    
    fitter = TextFitter()
    
    long_text = "This is a very long sentence that should be truncated intelligently. It contains multiple sentences. The system should try to break at sentence boundaries when possible. Korean text: 이것은 한국어 문장입니다. 지능적으로 잘라야 합니다."
    
    test_lengths = [50, 100, 150, 200]
    
    for length in test_lengths:
        print(f"\nTruncating to {length} characters:")
        
        # Smart truncation
        smart_result = fitter.truncate_with_ellipsis(
            long_text, length, smart_truncation=True, preserve_sentences=True
        )
        
        # Simple truncation for comparison
        simple_result = fitter.truncate_with_ellipsis(
            long_text, length, smart_truncation=False
        )
        
        print(f"Smart:  '{smart_result}'")
        print(f"Simple: '{simple_result}'")
        print(f"Smart length: {len(smart_result)}, Simple length: {len(simple_result)}")


def test_language_detection():
    """Test language detection and specific processing"""
    print("\n" + "=" * 60)
    print("Testing Language Detection & Processing")
    print("=" * 60)
    
    fitter = TextFitter()
    
    test_texts = [
        ("English text for testing", "english"),
        ("한국어 텍스트 테스트입니다", "korean"),
        ("中文测试文本", "chinese"),
        ("Mixed 한국어 and English text", "mixed"),
    ]
    
    for text, expected in test_texts:
        detected = fitter._detect_text_language(text)
        print(f"Text: '{text[:30]}...' -> Detected: {detected} (Expected: {expected})")
        
        # Test line breaking for each language
        broken = fitter.smart_line_break(text, 20, language_aware=True)
        print(f"Line break result: {broken.replace(chr(10), ' | ')}")
        print()


def test_performance():
    """Test performance improvements and caching"""
    print("\n" + "=" * 60)
    print("Testing Performance & Caching")
    print("=" * 60)
    
    fitter = TextFitter()
    
    # Performance test texts
    test_texts = [
        "Short text",
        "Medium length text for performance testing with some complexity",
        "Very long text " * 20 + " with repetitive content for stress testing",
        "한국어 성능 테스트 텍스트입니다. " * 10,
        "Mixed performance test 한글과 영어 텍스트 " * 15
    ]
    
    print("Running performance benchmark...")
    
    try:
        benchmark_results = fitter.benchmark_performance(test_texts, iterations=10)
        
        print("Performance Results:")
        for metric, value in benchmark_results.items():
            if 'ms' in metric:
                print(f"[OK] {metric}: {value:.2f}ms")
            else:
                print(f"[OK] {metric}: {value}")
                
    except Exception as e:
        print(f"[ERROR] Benchmark failed: {e}")
    
    # Test caching
    print(f"\nCache metrics before test:")
    metrics = fitter.get_performance_metrics()
    print(f"[OK] Cache hit rate: {metrics['cache_hit_rate']:.1f}%")
    print(f"[OK] Font cache size: {metrics['font_cache_size']}")
    print(f"[OK] Measurement cache size: {metrics['measurement_cache_size']}")


def test_advanced_features():
    """Test advanced features like density analysis and multi-column"""
    print("\n" + "=" * 60)
    print("Testing Advanced Features")
    print("=" * 60)
    
    fitter = TextFitter()
    
    test_text = """McKinsey & Company is a global management consulting firm. 
    We help organizations create positive, enduring change to accelerate their performance. 
    Our teams work with clients across industries and functions to drive transformation."""
    
    # Test optimal font size calculation
    print("Testing optimal font size calculation...")
    try:
        optimal_result = fitter.calculate_optimal_font_size(
            test_text, 4.0, 3.0, target_density=0.7
        )
        
        print(f"[OK] Optimal font size: {optimal_result['optimal_font_size']}pt")
        print(f"[OK] Text density: {optimal_result['text_density']:.3f}")
        print(f"[OK] Complexity score: {optimal_result['complexity_score']:.3f}")
        print(f"[OK] Readability score: {optimal_result['readability_score']:.3f}")
        
    except Exception as e:
        print(f"[ERROR] Optimal font size calculation failed: {e}")
    
    # Test multi-column layout
    print(f"\nTesting multi-column text splitting...")
    try:
        columns = fitter.split_text_to_columns(
            test_text, num_columns=2, box_width=6.0, 
            box_height=4.0, font_size=12
        )
        
        print(f"[OK] Split into {len(columns)} columns")
        for i, column in enumerate(columns):
            print(f"Column {i+1}: '{column[:50]}...'")
            
    except Exception as e:
        print(f"[ERROR] Multi-column splitting failed: {e}")
        
    # Test enhanced bullet spacing
    print(f"\nTesting enhanced bullet spacing...")
    try:
        spacing = fitter.calculate_bullet_spacing(5, 3.0, 14)
        print(f"[OK] Bullet spacing results:")
        for key, value in spacing.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"[ERROR] Bullet spacing calculation failed: {e}")


def main():
    """Run all tests"""
    print("Enhanced TextFitter Test Suite")
    print("Testing all new features and improvements...")
    
    try:
        # Run all test suites
        fitter = test_basic_functionality()
        test_text_fitting()
        test_smart_truncation()
        test_language_detection()
        test_performance()
        test_advanced_features()
        
        print("\n" + "=" * 60)
        print("Test Suite Completed Successfully!")
        print("=" * 60)
        
        # Final metrics
        final_metrics = fitter.get_performance_metrics()
        print(f"\nFinal Performance Metrics:")
        for key, value in final_metrics.items():
            print(f"[OK] {key}: {value}")
            
    except Exception as e:
        print(f"\n[ERROR] Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()