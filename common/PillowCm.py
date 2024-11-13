from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
from typing import Tuple, List, Optional, Union, Dict, Any
import os
import io
import logging
from datetime import datetime
from dataclasses import dataclass
import numpy as np
from pathlib import Path
import tempfile
from functools import wraps
from contextlib import contextmanager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='image_processing.log'
)
logger = logging.getLogger(__name__)

@dataclass
class ImageConfig:
    """이미지 처리 설정"""
    max_size: Tuple[int, int] = (1920, 1080)
    quality: int = 85
    format: str = 'JPEG'
    temp_dir: str = tempfile.gettempdir()

class ImageProcessor:
    """이미지 처리 기본 클래스"""
    def __init__(self, config: ImageConfig):
        self.config = config
    
    @staticmethod
    def load_image(source: Union[str, bytes, Image.Image]) -> Image.Image:
        """이미지 로드"""
        if isinstance(source, str):
            return Image.open(source)
        elif isinstance(source, bytes):
            return Image.open(io.BytesIO(source))
        elif isinstance(source, Image.Image):
            return source
        raise ValueError("Unsupported image source type")
    
    def save_image(self, image: Image.Image, path: str, **kwargs):
        """이미지 저장"""
        save_kwargs = {
            'quality': self.config.quality,
            'format': self.config.format
        }
        save_kwargs.update(kwargs)
        image.save(path, **save_kwargs)

class ImageResizer:
    """이미지 크기 조정"""
    @staticmethod
    def resize_to_fit(image: Image.Image, size: Tuple[int, int], 
                     maintain_aspect: bool = True) -> Image.Image:
        """크기에 맞게 조정"""
        if maintain_aspect:
            image.thumbnail(size, Image.Resampling.LANCZOS)
            return image
        return image.resize(size, Image.Resampling.LANCZOS)
    
    @staticmethod
    def resize_to_fill(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """크기에 맞게 채우기"""
        aspect_ratio = image.size[0] / image.size[1]
        target_ratio = size[0] / size[1]
        
        if aspect_ratio > target_ratio:
            height = size[1]
            width = int(height * aspect_ratio)
        else:
            width = size[0]
            height = int(width / aspect_ratio)
        
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        
        left = (width - size[0]) // 2
        top = (height - size[1]) // 2
        right = left + size[0]
        bottom = top + size[1]
        
        return resized.crop((left, top, right, bottom))

class ImageFilter:
    """이미지 필터 적용"""
    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
        """밝기 조정"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
        """대비 조정"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
        """채도 조정"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def apply_blur(image: Image.Image, radius: int) -> Image.Image:
        """블러 효과 적용"""
        return image.filter(ImageFilter.GaussianBlur(radius))
    
    @staticmethod
    def apply_sharpen(image: Image.Image) -> Image.Image:
        """선명도 증가"""
        return image.filter(ImageFilter.SHARPEN)

class ImageDrawer:
    """이미지 그리기 및 텍스트 추가"""
    def __init__(self, image: Image.Image):
        self.image = image
        self.draw = ImageDraw.Draw(image)
    
    def add_text(self, text: str, position: Tuple[int, int], 
                font_size: int = 24, color: str = 'white', 
                font_path: Optional[str] = None):
        """텍스트 추가"""
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
        
        self.draw.text(position, text, font=font, fill=color)
    
    def add_rectangle(self, bbox: Tuple[int, int, int, int], 
                     color: str = 'red', width: int = 2):
        """사각형 그리기"""
        self.draw.rectangle(bbox, outline=color, width=width)
    
    def add_watermark(self, watermark: Image.Image, position: str = 'center', 
                     opacity: float = 0.5):
        """워터마크 추가"""
        if opacity != 1:
            watermark.putalpha(int(255 * opacity))
        
        if position == 'center':
            x = (self.image.width - watermark.width) // 2
            y = (self.image.height - watermark.height) // 2
        elif position == 'bottom-right':
            x = self.image.width - watermark.width - 10
            y = self.image.height - watermark.height - 10
        else:
            x, y = 10, 10
        
        self.image.paste(watermark, (x, y), watermark)

class ImageTransformer:
    """이미지 변환"""
    @staticmethod
    def rotate(image: Image.Image, angle: float, 
              expand: bool = False) -> Image.Image:
        """회전"""
        return image.rotate(angle, expand=expand)
    
    @staticmethod
    def flip_horizontal(image: Image.Image) -> Image.Image:
        """수평 뒤집기"""
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    @staticmethod
    def flip_vertical(image: Image.Image) -> Image.Image:
        """수직 뒤집기"""
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    
    @staticmethod
    def crop(image: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
        """자르기"""
        return image.crop(box)

class ImageAnalyzer:
    """이미지 분석"""
    @staticmethod
    def get_histogram(image: Image.Image) -> Dict[str, List[int]]:
        """히스토그램 분석"""
        return {
            'red': image.histogram()[:256],
            'green': image.histogram()[256:512],
            'blue': image.histogram()[512:]
        }
    
    @staticmethod
    def get_dominant_color(image: Image.Image) -> Tuple[int, int, int]:
        """주요 색상 추출"""
        colors = image.getcolors(image.size[0] * image.size[1])
        if not colors:
            return (0, 0, 0)
        
        sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)
        return sorted_colors[0][1]
    
    @staticmethod
    def calculate_average_brightness(image: Image.Image) -> float:
        """평균 밝기 계산"""
        grayscale = image.convert('L')
        return sum(grayscale.getdata()) / (image.size[0] * image.size[1])

class BatchProcessor:
    """배치 이미지 처리"""
    def __init__(self, config: ImageConfig):
        self.config = config
    
    def process_directory(self, input_dir: str, output_dir: str, 
                         operations: List[Dict[str, Any]]):
        """디렉토리 내 이미지 일괄 처리"""
        os.makedirs(output_dir, exist_ok=True)
        
        for filename in os.listdir(input_dir):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                image = Image.open(input_path)
                
                for operation in operations:
                    func = operation['function']
                    params = operation.get('params', {})
                    image = func(image, **params)
                
                image.save(output_path, quality=self.config.quality)
                logger.info(f"Processed {filename}")
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")

class ImageOptimizer:
    """이미지 최적화"""
    @staticmethod
    def compress_image(image: Image.Image, quality: int = 85) -> Image.Image:
        """이미지 압축"""
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        return Image.open(output)
    
    @staticmethod
    def convert_format(image: Image.Image, format: str = 'WEBP') -> Image.Image:
        """형식 변환"""
        output = io.BytesIO()
        image.save(output, format=format)
        return Image.open(output)
    
    @staticmethod
    def reduce_colors(image: Image.Image, colors: int = 256) -> Image.Image:
        """색상 수 감소"""
        return image.quantize(colors)

class ImageFramework:
    """통합 이미지 처리 프레임워크"""
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
    
    def load_image(self, source: Union[str, bytes, Image.Image]) -> Image.Image:
        """이미지 로드"""
        return self.processor.load_image(source)
    
    def save_image(self, image: Image.Image, path: str, **kwargs):
        """이미지 저장"""
        self.processor.save_image(image, path, **kwargs)
    
    def create_drawer(self, image: Image.Image) -> ImageDrawer:
        """드로어 생성"""
        return ImageDrawer(image)

# 사용 예시
def example_usage():
    # 설정
    config = ImageConfig(
        max_size=(1920, 1080),
        quality=85,
        format='JPEG'
    )
    
    # 프레임워크 초기화
    image_framework = ImageFramework(config)
    
    # 이미지 로드
    image = image_framework.load_image("input.jpg")
    
    # 크기 조정
    image = image_framework.resizer.resize_to_fit(image, (800, 600))
    
    # 필터 적용
    image = image_framework.filter.adjust_brightness(image, 1.2)
    image = image_framework.filter.adjust_contrast(image, 1.1)
    
    # 워터마크 추가
    drawer = image_framework.create_drawer(image)
    drawer.add_text("Copyright 2024", (10, 10), font_size=24)
    
    # 이미지 분석
    histogram = image_framework.analyzer.get_histogram(image)
    dominant_color = image_framework.analyzer.get_dominant_color(image)
    
    # 최적화 및 저장
    image = image_framework.optimizer.compress_image(image, quality=85)
    image_framework.save_image(image, "output.jpg")

if __name__ == "__main__":
    example_usage()
