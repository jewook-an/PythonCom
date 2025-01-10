#### # 로깅
1. 로깅 설정
```
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       filename='image_processing.log')
   logger = logging.getLogger(__name__)
```
#### # Dataclass
1. ImageConfig : 이미지 처리 설정
    - max_size
    - quality
    - format
    - temp_dir

2. ImageProcessor : 이미지 처리 기본 클래스
    - Config
    ```
    def __init__(self, config: ImageConfig):
        self.config = config
    ```

    - staticmethod
        - load_image(source: Union[str, bytes, Image.Image]) : 이미지 로드
    - save_image(self, image: Image.Image, path: str, **kwargs) : 이미지 저장

3. ImageResizer : 이미지 크기 조정
    - staticmethod
        - resize_to_fit(image: Image.Image, size: Tuple[int, int], maintain_aspect: bool = True) : 크기에 맞게 조정
        - resize_to_fill(image: Image.Image, size: Tuple[int, int]) : 크기에 맞게 채우기

4. ImageFilter : 이미지 필터 적용
    - staticmethod
        - adjust_brightness(image: Image.Image, factor: float) : 밝기 조정
        - adjust_contrast(image: Image.Image, factor: float) : 대비 조정
        - adjust_saturation(image: Image.Image, factor: float) : 채도 조정
        - apply_blur(image: Image.Image, radius: int) : 블러 효과 적용
        - apply_sharpen(image: Image.Image) : 선명도 증가

5. ImageDrawer : 이미지 그리기 및 텍스트 추가
    ```
    def __init__(self, image: Image.Image):
        self.image = image
        self.draw = ImageDraw.Draw(image)
    ```

    - add_text(self, text: str, position: Tuple[int, int], font_size: int = 24, color: str = 'white', font_path: Optional[str] = None) : 텍스트 추가
    - add_rectangle(self, bbox: Tuple[int, int, int, int], color: str = 'red', width: int = 2) : 사각형 그리기
    - add_watermark(self, watermark: Image.Image, position: str = 'center', opacity: float = 0.5) : 워터마크 추가

6. ImageTransformer : 이미지 변환
    - staticmethod
        - rotate(image: Image.Image, angle: float, expand: bool = False) : 회전
        - flip_horizontal(image: Image.Image) : 수평 뒤집기
        - flip_vertical(image: Image.Image) : 수직 뒤집기
        - crop(image: Image.Image, box: Tuple[int, int, int, int]) : 자르기

7. class ImageAnalyzer : 이미지 분석
    - staticmethod
        - get_histogram(image: Image.Image) -> Dict[str, List[int]]: 히스토그램 분석
        - get_dominant_color(image: Image.Image) -> Tuple[int, int, int]: 주요 색상 추출
        - calculate_average_brightness(image: Image.Image) -> float: 평균 밝기 계산

8. class BatchProcessor: 배치 이미지 처리
    ```
    def __init__(self, config: ImageConfig):
        self.config = config
    ```

    - process_directory(self, input_dir: str, output_dir: str, operations: List[Dict[str, Any]]): 디렉토리 내 이미지 일괄 처리

10. class ImageOptimizer : 이미지 최적화
    - staticmethod
        - compress_image(image: Image.Image, quality: int = 85) : 이미지 압축
        - convert_format(image: Image.Image, format: str = 'WEBP') : 형식 변환
        - reduce_colors(image: Image.Image, colors: int = 256) : 색상 수 감소

11. class ImageFramework : 통합 이미지 처리 프레임워크
    ```
    def __init__(self, config: Optional[ImageConfig] = None):
        self.config = config or ImageConfig()

        # 각 컴포넌트 초기화
        self.processor = ImageProcessor(self.config)
        self.resizer = ImageResizer()
        self.filter = ImageFilter()
        self.transformer = ImageTransformer()
        self.analyzer = ImageAnalyzer()
        self.optimizer = ImageOptimizer()
        self.batch_processor = BatchProcessor(self.config)
    ```
    - load_image(self, source: Union[str, bytes, Image.Image]) : 이미지 로드
    - save_image(self, image: Image.Image, path: str, **kwargs): 이미지 저장
    - create_drawer(self, image: Image.Image) -> ImageDrawer: 드로어 생성





