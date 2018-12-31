#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class libuiConan(ConanFile):
    name = "libui"
    version = "0.4.1"
    description = "Keep it short"
    topics = ("conan", "libui", "ui", "gui")
    url = "https://github.com/bincrafters/conan-libui"
    homepage = "https://github.com/andlabs/libui"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT" 
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        url_version = "alpha4.1"
        tools.get(
            "{0}/archive/{1}.tar.gz".format(self.homepage, url_version), 
            sha256="f51a9e20e9f9a4c0bce1571ee37f203f42de33e3ac7359a6aac87a54798e8716")
        extracted_dir = self.name + "-" + url_version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.h", dst="include", src=self._source_subfolder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if(self.settings.os == "Windows"):
            self.cpp_info.libs.extend([
                "user32",
                "kernel32",
                "gdi32",
                "comctl32",
                "msimg32",
                "comdlg32",
                "d2d1",
                "dwrite",
                "ole32",
                "oleaut32",
                "oleacc",
                "uuid",
                "windowscodecs",
            ])
            
            
            