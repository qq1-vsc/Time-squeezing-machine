import json
import os
from pathlib import Path

class ConfigManager:
    """配置文件管理器 - 持久化保存 API Key 和其他设置"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value
        self.save_config()
    
    def get_api_key(self):
        """获取 API Key"""
        return self.get('deepseek_api_key', '')
    
    def set_api_key(self, api_key):
        """保存 API Key"""
        self.set('deepseek_api_key', api_key)
    
    def has_api_key(self):
        """检查是否已保存 API Key"""
        return bool(self.get_api_key())
