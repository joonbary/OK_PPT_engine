import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUI 없는 환경
from typing import Dict, List
import os
import logging

logger = logging.getLogger(__name__)


class ChartGenerator:
    """McKinsey 스타일 차트 생성기"""
    
    def __init__(self):
        self.output_dir = "/app/temp_charts"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # McKinsey 색상 팔레트
        self.colors = {
            'primary': '#0076A8',      # McKinsey Blue
            'secondary': '#F47621',    # Orange
            'positive': '#6BA644',     # Green
            'negative': '#E31B23',     # Red
            'neutral': '#53565A'       # Gray
        }
        
        # color_sequence 추가 (stacked_bar_chart에서 사용)
        self.color_sequence = ['#0076A8', '#F47621', '#6BA644', '#E31B23', '#53565A']
        
        logger.info("ChartGenerator initialized")
    
    def generate_chart(self, chart_spec: Dict) -> str:
        """
        차트 생성 및 이미지 파일 경로 반환
        
        Args:
            chart_spec: {
                'type': 'bar' | 'line' | 'pie' | 'waterfall',
                'data': {...},
                'title': str,
                'id': str
            }
        
        Returns:
            이미지 파일 절대 경로
        """
        chart_type = chart_spec.get('type', 'bar')
        
        logger.info(f"차트 생성 시작: {chart_type} - {chart_spec.get('title', 'Untitled')}")
        
        try:
            if chart_type == 'bar':
                filepath = self._create_bar_chart(chart_spec)
            elif chart_type == 'line':
                filepath = self._create_line_chart(chart_spec)
            elif chart_type == 'pie':
                filepath = self._create_pie_chart(chart_spec)
            elif chart_type == 'waterfall':
                filepath = self._create_waterfall_chart(chart_spec)
            else:
                filepath = self._create_bar_chart(chart_spec)
            
            logger.info(f"차트 생성 완료: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"차트 생성 실패: {e}")
            raise
    
    def _create_bar_chart(self, spec: Dict) -> str:
        """막대 차트 생성"""
        fig, ax = plt.subplots(figsize=(8, 5))
        
        data = spec.get('data', {})
        categories = data.get('categories', ['A', 'B', 'C', 'D'])
        values = data.get('values', [30, 45, 25, 50])
        
        # 막대 그래프
        bars = ax.bar(categories, values, color=self.colors['primary'], width=0.6)
        
        # 값 레이블
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=11,
                fontweight='bold'
            )
        
        # 스타일 설정
        title = spec.get('title', 'Chart')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # 저장
        filepath = os.path.join(self.output_dir, f"chart_{spec.get('id', 'temp')}.png")
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def _create_line_chart(self, spec: Dict) -> str:
        """선 차트 생성"""
        fig, ax = plt.subplots(figsize=(8, 5))
        
        data = spec.get('data', {})
        x_data = data.get('x', ['Q1', 'Q2', 'Q3', 'Q4'])
        y_data = data.get('y', [20, 35, 30, 45])
        
        # 선 그래프
        ax.plot(
            x_data, y_data,
            color=self.colors['primary'],
            linewidth=3,
            marker='o',
            markersize=8,
            markerfacecolor=self.colors['primary'],
            markeredgecolor='white',
            markeredgewidth=2
        )
        
        # 값 레이블
        for i, (x, y) in enumerate(zip(x_data, y_data)):
            ax.text(
                i, y + 2,
                f'{int(y)}',
                ha='center',
                fontsize=10,
                fontweight='bold'
            )
        
        # 스타일
        title = spec.get('title', 'Trend Analysis')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        filepath = os.path.join(self.output_dir, f"chart_{spec.get('id', 'temp')}.png")
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def _create_pie_chart(self, spec: Dict) -> str:
        """파이 차트 생성"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        data = spec.get('data', {})
        labels = data.get('labels', ['A', 'B', 'C', 'D'])
        sizes = data.get('sizes', [30, 25, 20, 25])
        
        colors = [
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['positive'],
            self.colors['neutral']
        ]
        
        # 파이 차트
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        
        # 스타일
        for autotext in autotexts:
            autotext.set_color('white')
        
        title = spec.get('title', 'Distribution')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        filepath = os.path.join(self.output_dir, f"chart_{spec.get('id', 'temp')}.png")
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def _create_waterfall_chart(self, spec: Dict) -> str:
        """워터폴 차트 생성 (McKinsey 필수)"""
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        data = spec.get('data', {})
        categories = data.get('categories', ['Start', 'Inc1', 'Inc2', 'Dec1', 'End'])
        values = data.get('values', [100, 20, 15, -10, 125])
        
        # Ensure categories and values have the same length
        if len(categories) != len(values):
            raise ValueError("Categories and values must have the same number of elements for waterfall chart.")

        # Calculate the 'bottom' and 'height' for each bar
        # The first bar is the starting value
        # Intermediate bars are changes
        # The last bar is the final total

        # Initialize lists for heights and bottoms
        heights = []
        bottoms = []
        running_total = 0

        for i, val in enumerate(values):
            if i == 0:  # First bar (Start)
                heights.append(val)
                bottoms.append(0)
                running_total = val
            elif i == len(values) - 1:  # Last bar (End)
                heights.append(val)
                bottoms.append(0)
            else:  # Intermediate bars (Increments/Decrements)
                heights.append(val)
                bottoms.append(running_total)
                running_total += val

        # 막대 색상
        colors_list = []
        for i, val in enumerate(values):
            if i == 0 or i == len(values) - 1: # Start and End bars are primary color
                colors_list.append(self.colors['primary'])
            elif val > 0:
                colors_list.append(self.colors['positive'])
            elif val < 0:
                colors_list.append(self.colors['negative'])
            else:
                colors_list.append(self.colors['neutral'])
        
        # 워터폴 막대
        bars = ax.bar(
            range(len(categories)),
            heights,
            bottom=bottoms,
            color=colors_list,
            width=0.6
        )
        
        # 값 레이블
        for i, (bar, val) in enumerate(zip(bars, values)):
            y_pos = bar.get_y() + bar.get_height() / 2
            
            label = f'{int(val)}'
            if i > 0 and i < len(values) - 1: # Only for intermediate changes, show +/- sign
                label = f'+{int(val)}' if val > 0 else f'{int(val)}'
            
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                y_pos,
                label,
                ha='center',
                va='center',
                fontsize=11,
                fontweight='bold',
                color='white' if bar.get_height() != 0 else 'black' # Label color based on bar height
            )
        
        # 연결선
        for i in range(len(categories) - 1):
            x_start = i + 0.3
            x_end = i + 0.7
            y = bottoms[i+1] if i < len(bottoms) - 1 else running_total # Use the bottom of the next bar for connection
            ax.plot([x_start, x_end], [y, y], 'k--', linewidth=1, alpha=0.5)
        
        # 스타일
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=0)
        
        title = spec.get('title', 'Waterfall Analysis')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        filepath = os.path.join(self.output_dir, f"chart_{spec.get('id', 'temp')}.png")
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def _generate_sample_data(self, chart_type: str) -> Dict:
        """차트 타입에 따른 샘플 데이터 생성"""
        if chart_type == 'bar':
            return {
                'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
                'values': [random.randint(20, 80) for _ in range(4)]
            }
        elif chart_type == 'line':
            return {
                'x': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'y': [random.randint(15, 60) for _ in range(6)]
            }
        elif chart_type == 'pie':
            return {
                'labels': ['Product A', 'Product B', 'Product C', 'Product D'],
                'sizes': [random.randint(15, 35) for _ in range(4)]
            }
        elif chart_type == 'waterfall':
            return {
                'categories': ['Start', 'Revenue', 'Cost', 'Tax', 'End'],
                'values': [100, 50, -30, -10, 110]
            }
        elif chart_type == 'stacked_bar':
            return {
                'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
                'series1': [random.randint(10, 30) for _ in range(4)],
                'series2': [random.randint(15, 35) for _ in range(4)],
                'series3': [random.randint(20, 40) for _ in range(4)]
            }
        else:
            return {}
    
    def _create_stacked_bar_chart(self, spec: Dict) -> str:
        """적층 막대 차트 생성"""
        fig, ax = plt.subplots(figsize=(8, 5))
        
        data = spec.get('data', {})
        categories = data.get('categories', ['Q1', 'Q2', 'Q3', 'Q4'])
        
        # 시리즈 데이터 처리
        series_data = []
        series_labels = []
        for key in data:
            if key.startswith('series'):
                series_data.append(data[key])
                series_labels.append(key.replace('series', 'Series '))
        
        if not series_data:
            series_data = [
                [20, 25, 30, 35],
                [15, 20, 25, 30],
                [10, 15, 20, 25]
            ]
            series_labels = ['Series 1', 'Series 2', 'Series 3']
        
        # 적층 막대
        x = np.arange(len(categories))
        width = 0.6
        bottom = np.zeros(len(categories))
        
        bars = []
        for i, (data_series, label) in enumerate(zip(series_data, series_labels)):
            bar = ax.bar(x, data_series, width, label=label,
                        bottom=bottom, color=self.color_sequence[i % len(self.color_sequence)])
            bars.append(bar)
            bottom += data_series
        
        # 스타일
        ax.set_xlabel(spec.get('x_label', ''))
        ax.set_ylabel(spec.get('y_label', 'Value'))
        ax.set_title(spec.get('title', 'Stacked Bar Analysis'), fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend(loc='upper right')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
        filepath = os.path.join(self.output_dir, f"chart_{spec.get('id', 'temp')}.png")
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        return filepath
    
    def _create_combo_chart(self, spec: Dict) -> str:
        """콤보 차트 (막대 + 선) 생성"""
        fig, ax1 = plt.subplots(figsize=(8, 5))
        
        data = spec.get('data', {})
        categories = data.get('categories', ['Q1', 'Q2', 'Q3', 'Q4'])
        bar_values = data.get('bar_values', [40, 45, 50, 55])
        line_values = data.get('line_values', [20, 22, 25, 28])
        
        x = np.arange(len(categories))
        width = 0.6
        
        # 막대 차트 (왼쪽 축)
        bars = ax1.bar(x, bar_values, width, color=self.colors['primary'], alpha=0.8, label='Revenue')
        ax1.set_xlabel(spec.get('x_label', 'Period'))
        ax1.set_ylabel('Revenue ($M)', color=self.colors['primary'])
        ax1.tick_params(axis='y', labelcolor=self.colors['primary'])
        
        # 선 차트 (오른쪽 축)
        ax2 = ax1.twinx()
        line = ax2.plot(x, line_values, color=self.colors['negative'], marker='o', linewidth=2.5, label='Margin %')
        ax2.set_ylabel('Margin (%)', color=self.colors['negative'])
        ax2.tick_params(axis='y', labelcolor=self.colors['negative'])
        
        # 공통 스타일
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.set_title(spec.get('title', 'Revenue & Margin Analysis'), fontweight='bold', pad=20)
        ax1.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_axisbelow(True)
        
        # 범례
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        filepath = os.path.join(self.output_dir, f"chart_{spec.get('id', 'temp')}.png")
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        return filepath
    
    def _create_fallback_chart(self, spec: Dict) -> str:
        """실패 시 기본 차트 생성"""
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # 기본 막대 차트
        categories = ['A', 'B', 'C', 'D']
        values = [25, 40, 30, 45]
        
        bars = ax.bar(categories, values, color=self.colors['primary'], width=0.6)
        
        ax.set_title(spec.get('title', 'Chart'), fontsize=14, fontweight='bold', pad=20)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
        filepath = os.path.join(self.output_dir, f"chart_{spec.get('id', 'fallback')}.png")
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        return filepath