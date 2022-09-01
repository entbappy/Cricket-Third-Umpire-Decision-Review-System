import os
import sys
from review_system.logger.log import logging
from review_system.utils.util import read_yaml_file
from review_system.exception.exception_handler import AppException
from review_system.entity.config_entity import TemplatesConfig, RootAppConfig


ROOT_DIR = os.getcwd()
# Main config file path
CONFIG_FOLDER_NAME = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_FOLDER_NAME,CONFIG_FILE_NAME)


class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e

    
    def get_templates_config(self) -> TemplatesConfig:
        try:
            templates_config = self.configs_info['templates_config']
            templates_dir = templates_config['templates_dir']

            clips_dir = os.path.join(templates_dir, templates_config['clips_dir'])
            sprites_dir = os.path.join(templates_dir, templates_config['sprites_dir'])
            clip_name = templates_config['clip_name']

            response = TemplatesConfig(
                clips_dir = clips_dir,
                sprites_dir = sprites_dir,
                clip_name = clip_name
            )

            logging.info(f"Templates config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e


    
    def get_root_app_config(self) -> RootAppConfig:
        try:
            root_game_config = self.configs_info['root_app_config']

            screen_width = root_game_config['screen_width']
            screen_height = root_game_config['screen_height']
        
            response = RootAppConfig(
                screen_width = screen_width,
                screen_height = screen_height
            )

            logging.info(f"Root config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

