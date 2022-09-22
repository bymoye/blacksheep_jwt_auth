from dataclasses import asdict, dataclass
import os, yaml


@dataclass
class Gconfig:
    password: str
    salt: str

    def __init__(self) -> None:
        self.init()
        print('初始化完成')

    # 初始化
    def init(self) -> None:
        print('初始化配置文件')
        try:
            if not os.path.exists('config.yaml'):
                raise FileNotFoundError('Config 文件不存在')
            with open('config.yaml') as f:
                config: dict = yaml.safe_load(f)
                assert config and config.get('password') and \
                    config.get('salt'), 'config 文件不完整'

                self.password = config['password']
                self.salt = config['salt']
        except FileNotFoundError as e:
            print(f'Error: {e}')
            print('创建config.yaml')
            with open('config.yaml', 'w') as f:
                self.password = input('请键入password(加密用): ')
                self.salt = os.urandom(16).hex()
                f.write(yaml.safe_dump(asdict(self)))
                print('文件写入成功,请勿泄露妥善保管,请勿修改config.yaml,否则会造成严重后果.')
        except AssertionError as e:
            print(f'Error: {e}')
            self.fix_config()

    # 修复config.yaml
    def fix_config(self) -> None:
        print('尝试检查 config.yaml')
        with open('config.yaml', 'r+') as f:
            config: dict = yaml.safe_load(f)
            self.password = config['password'] \
                if config and config.get('password') else \
                input('请键入password(加密用): ')
            self.salt = config['salt'] \
                if config and config.get('salt') else \
                os.urandom(16).hex()
            f.seek(0)
            f.write(yaml.safe_dump(asdict(self)))
