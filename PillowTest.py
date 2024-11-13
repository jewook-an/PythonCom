from PIL import Image
from pathlib import Path
import tempfile

# ImageConfig와 ImageFramework 임포트 (이전 코드에서 정의됨)
# from pillow_framework import ImageConfig, ImageFramework

def demo_image_processing():
    """Pillow 프레임워크 사용 예시 데모"""
    
    # 1. 기본 설정
    config = ImageConfig(
        max_size=(1920, 1080),
        quality=85,
        format='JPEG',
        temp_dir=tempfile.gettempdir()
    )
    
    # 2. 프레임워크 초기화
    framework = ImageFramework(config)
    
    # 예시 이미지 경로 설정
    input_path = "input_image.jpg"  # 실제 이미지 경로로 변경하세요
    output_dir = Path("processed_images")
    output_dir.mkdir(exist_ok=True)
    
    # 3. 단일 이미지 처리 예시
    def process_single_image():
        # 이미지 로드
        image = framework.load_image(input_path)
        
        # 이미지 리사이징
        resized_image = framework.resizer.resize_to_fit(image, (800, 600))
        framework.save_image(resized_image, output_dir / "resized.jpg")
        
        # 이미지 채우기 (crop to fill)
        filled_image = framework.resizer.resize_to_fill(image, (500, 500))
        framework.save_image(filled_image, output_dir / "filled.jpg")
        
        # 필터 적용
        brightened = framework.filter.adjust_brightness(image, 1.2)
        framework.save_image(brightened, output_dir / "brightened.jpg")
        
        contrasted = framework.filter.adjust_contrast(image, 1.3)
        framework.save_image(contrasted, output_dir / "contrasted.jpg")
        
        saturated = framework.filter.adjust_saturation(image, 1.5)
        framework.save_image(saturated, output_dir / "saturated.jpg")
        
        blurred = framework.filter.apply_blur(image, radius=2)
        framework.save_image(blurred, output_dir / "blurred.jpg")
        
        # 이미지 변환
        rotated = framework.transformer.rotate(image, angle=45, expand=True)
        framework.save_image(rotated, output_dir / "rotated.jpg")
        
        flipped = framework.transformer.flip_horizontal(image)
        framework.save_image(flipped, output_dir / "flipped.jpg")
        
        # 이미지에 텍스트와 도형 추가
        draw_image = image.copy()
        drawer = framework.create_drawer(draw_image)
        drawer.add_text("Hello, Pillow!", (50, 50), font_size=36, color='white')
        drawer.add_rectangle((100, 100, 300, 200), color='red', width=3)
        framework.save_image(draw_image, output_dir / "drawn.jpg")
        
        # 워터마크 추가 (워터마크 이미지가 필요)
        try:
            watermark = framework.load_image("watermark.png")
            watermarked = image.copy()
            drawer = framework.create_drawer(watermarked)
            drawer.add_watermark(watermark, position='bottom-right', opacity=0.7)
            framework.save_image(watermarked, output_dir / "watermarked.jpg")
        except:
            print("워터마크 이미지가 없습니다.")
        
        return image  # 원본 이미지 반환 (분석용)

    # 4. 이미지 분석 예시
    def analyze_image(image):
        # 히스토그램 분석
        histogram = framework.analyzer.get_histogram(image)
        print("Color Histogram Summary:")
        for color, values in histogram.items():
            print(f"{color.capitalize()} channel - Max value: {max(values)}")
        
        # 주요 색상 추출
        dominant_color = framework.analyzer.get_dominant_color(image)
        print(f"\nDominant Color (RGB): {dominant_color}")
        
        # 평균 밝기 계산
        brightness = framework.analyzer.calculate_average_brightness(image)
        print(f"Average Brightness: {brightness:.2f}")

    # 5. 배치 처리 예시
    def batch_process_example():
        operations = [
            {
                'function': framework.resizer.resize_to_fit,
                'params': {'size': (800, 600)}
            },
            {
                'function': framework.filter.adjust_brightness,
                'params': {'factor': 1.1}
            },
            {
                'function': framework.filter.adjust_contrast,
                'params': {'factor': 1.2}
            }
        ]
        
        framework.batch_processor.process_directory(
            input_dir="input_images",  # 입력 이미지들이 있는 디렉토리
            output_dir="output_images",  # 출력될 디렉토리
            operations=operations
        )

    # 6. 이미지 최적화 예시
    def optimize_image(image):
        # 이미지 압축
        compressed = framework.optimizer.compress_image(image, quality=75)
        framework.save_image(compressed, output_dir / "compressed.jpg")
        
        # WebP 형식으로 변환
        webp_image = framework.optimizer.convert_format(image, format='WEBP')
        framework.save_image(webp_image, output_dir / "converted.webp")
        
        # 색상 수 감소
        reduced_colors = framework.optimizer.reduce_colors(image, colors=64)
        framework.save_image(reduced_colors, output_dir / "reduced_colors.png")

    # 모든 예시 실행
    try:
        print("Processing single image...")
        original_image = process_single_image()
        
        print("\nAnalyzing image...")
        analyze_image(original_image)
        
        print("\nOptimizing image...")
        optimize_image(original_image)
        
        print("\nBatch processing images...")
        batch_process_example()
        
        print("\nAll processing completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    demo_image_processing()
