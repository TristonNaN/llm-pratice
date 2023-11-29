import os
import logging


class MyLogger:
    def __init__(self, name="pdf_translator", log_dir="logs", debug=False, save_to_file=False):
        # 设置日志级别
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger(name)

        # 清除先前的处理器
        self.logger.handlers = []

        if save_to_file:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_file_path = os.path.join(log_dir, f"{name}.log")

            # 设置文件处理器
            file_handler = logging.FileHandler(log_file_path, 'a', encoding='utf-8')  # mode='a' 追加模式
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            file_handler.setLevel(logging.DEBUG)

            # 将文件处理器添加到 logger
            self.logger.addHandler(file_handler)


logger = MyLogger(debug=True).logger

if __name__ == "__main__":
    logger = MyLogger().logger

    logger.debug("这是一条调试信息。")
    logger.info("这是一条信息。")
    logger.warning("这是一条警告信息。")
    logger.error("这是一条错误信息。")
