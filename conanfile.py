#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class VariantConan(ConanFile):
    name = "variant"
    version = "1.3.0"
    url = "https://github.com/bincrafters/conan-variant"
    description = "C++17 `std::variant` for C++11/14/17 https://mpark.github.io/variant"

    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"build_tests": [True, False]}
    default_options = "build_tests=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    # Use version ranges for dependencies unless there's a reason not to
    requires = (
        "gtest/[>=1.8.0]@jgsogo/testing",
    )

    def source(self):
        source_url = "https://github.com/mpark/variant"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        # Work to remove 'deps' directory (conan will handle them)
        shutil.rmtree(os.path.join(extracted_dir, "3rdparty"))
        tools.replace_in_file(os.path.join(extracted_dir, "test", "CMakeLists.txt"),
'''
  add_subdirectory(${CMAKE_SOURCE_DIR}/3rdparty/googletest/googletest
                   ${CMAKE_BINARY_DIR}/3rdparty/googletest/googletest)
''',
'''
  include(${CONAN_GTEST_ROOT}/cmake/internal_utils.cmake)
''')
        tools.replace_in_file(os.path.join(extracted_dir, "test", "CMakeLists.txt"), 'gtest_main', '${CONAN_LIBS_GTEST}')

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)


    def build(self):
        cmake = CMake(self)
        if self.options.build_tests:
            cmake.definitions["MPARK_VARIANT_INCLUDE_TESTS"] = "mpark"  # Adding 'libc++' will trigger an ExternalProjectAdd for llvm
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
    
    def package_id(self):
        self.info.header_only()

