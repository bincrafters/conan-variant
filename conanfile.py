from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os
import shutil


class VariantConan(ConanFile):
    name = "variant"
    version = "1.3.0"
    url = "https://github.com/bincrafters/conan-variant"
    homepage = "https://github.com/bincrafters/conan-variant"
    description = "C++17 std::variant for C++11/14/17"
    license = "BSL-1.0"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        if self.settings.compiler == "Visual Studio" and int(self.settings.compiler.version.value) <= 12:
            raise ConanInvalidConfiguration("Required MSVC 2015 Update 3 or superior")  # https://github.com/mpark/variant/blob/v1.3.0/include/mpark/config.hpp#L11

    def source(self):
        source_url = "https://github.com/mpark/variant"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        # Work to remove 'deps' directory, just to be sure.
        shutil.rmtree(os.path.join(extracted_dir, "3rdparty"))

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="license", src=self._source_subfolder)
    
    def package_id(self):
        self.info.header_only()
    
    def package_info(self):
        pass
