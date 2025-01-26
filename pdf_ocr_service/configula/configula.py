import io
import os.path

from tomlkit import loads


class Configula:
    """
    Create a single configuration by merging settings defined in:
     1. in environment variables
     2. in toml file
    Value provided in **environment variable have priority** over values from
    toml configuration file.
    By default all environment variables are prefixed with 'PDF-OCR'.
     By default '__" (two underscores) is used as delimiter in environment variables names.
     for example, given following toml file:
     [database]
        url=xxx@xxx
        user_name=ddd
        password=XXX
     [tmp-dir]
        path=/xxx/yy/dd
    [ocr]
       default_language = 'eng'

    corespondent environment variables names are  PDF-OCR__OCR__DEFAULT_LANGUAGE - notices two underscores
    separate section name from prefix and variable name. Environment variable name format is (all in uppercase):
      <prefix><delimiter><section><delimiter><variable>
    Although in toml files you can place variable names outside sections, in Configula all variables **must be placed in section** .
    By default Configula looks up for following toml files:
      - /etc/pdf-ocr-pdf_ocr_service/pdf-ocr-pdf_ocr_service.toml
      - /etc/pdf-ocr-pdf_ocr_service.toml
      - pdf-ocr-pdf_ocr_service.toml
    If you have custom location (or custom file name), use
    ``PDF-OCR__CONFIG`` environment variable to point to it:
    PDF-OCR__CONFIG =/app/config/pm.toml

     Example of usage:
       from configula import Configula
       config = Configula()

       default_language = config.get('ocr','default_language')
       debug = config.get('main','debug', default=False)

    """

    DEFAULT_PREFIX = 'PDF-OCR'
    DEFAULT_DELIMITER = '__'
    DEFAULT_LOCATIONS = [
        "/etc/pdf-ocr-service/pdf-ocr-service.toml",
        "/etc/pdf-ocr-service.toml",
        "pdf-ocr-service.toml",
        os.path.join(os.path.dirname(__file__), '../../tests', 'pdf-ocr-service.toml'),
    ]
    DEFAULT_CONFIG_VAR_NAME = 'PDF-OCR-CONFIG'

    def __init__(self,
                 prefix=None,
                 delimiter=None,
                 config_locations=None,
                 config_env_var_name=None
                 ):
        """

    `config_locations` (list): a list of string file paths
            where to load configurations from
        `config_env_var_name` (str): in case `config_locations` was
            not provided, load file configurations
        from a file pointed by this environment variable
        `prefix` (str): all configurations provided by environment
            variables will be prefixed with this value
        `delimiter` (str): default delimiter is `__` (two underscores)
            i.e. <prefix>__<section>__<value>

        Example:

            Configula(
                prefix='PDF-OCR',
                config_locations=[
                    'pdf-ocr-service.toml',
                    'pdf-ocr-service.toml'
                ],
                config_env_var_name='PDF-OCR-CONFIG'
            )

        In case pdf-ocr-service.toml was not found in current location
        and /etc/pdf-ocr-service.toml does not exists, it continue look for
        configuration file by looking at PDF-OCR-CONFIG environment
        variable. If PDF-OCR-CONFIG environment variable exists and is
        (for example):

            PDF-OCR__CONFIG=/home/eugen/pdf-ocr-pdf-service.toml

        will load configurations from /home/eugen/pdf-ocr-pdf-service.toml.

        Environment variables values have HIGHTEST priority.
        If both toml configuration file is present and corresponding
        environment variable is present - environment variable gets
        priority over corresponding value found in toml file.
        """
        if config_locations is None:
            self.config_locations = self.DEFAULT_LOCATIONS
        else:
            self.config_locations = config_locations

        if config_env_var_name is None:
            self.config_env_var_name = self.DEFAULT_CONFIG_VAR_NAME
        else:
            self.config_env_var_name = config_env_var_name

        if prefix is None:
            self.prefix = self.DEFAULT_PREFIX
        else:
            self.prefix = prefix

        if delimiter is None:
            self.delimiter = self.DEFAULT_DELIMITER
        else:
            self.delimiter = delimiter

        self._toml_config = self.load_toml()

    def load_toml(self):
        """
        Loads toml configuration file from self.config_locations or
        from location pointed by self.config_env_var_name.

        :return: None in case toml configuration file was not found. return a dictionary of
        configuration if toml config was found
        """
        for config_file in self.config_locations:
            if os.path.exists(config_file):
                os.environ["CONFIG_FILE"] = os.path.abspath(config_file)
                return Configula._loads(config_file)

        config_file = os.environ.get(self.DEFAULT_CONFIG_VAR_NAME, False)
        if config_file and os.path.exists(config_file):
            # print(f"Loading default config file: {config_file}")
            return Configula._loads(config_file)

    def get(self, section_name, var_name, default=None):
        """

        :param section_name:
        :param var_name:
        :param default:
        :return:
        """

        pref = self.prefix
        delim = self.delimiter

        env_name = f"{pref}{delim}{section_name}{delim}{var_name}".upper()

        try:
            env_value = os.getenv(env_name)
            value = env_value or self._toml_config[section_name][var_name]
        except Exception as _:
            value = default
        return value

    @classmethod
    def _loads(cls, file_path):
        with io.open(file_path, encoding="utf-8") as f:
            return loads(f.read())
