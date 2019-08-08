#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class Base64Conan(ConanFile):
    name = "base64"
    version = "1.0.2"
    creator = "DEGoodmanWilson"
    url = "https://github.com/DEGoodmanWilson/conan-base64".format(creator, name)
    description = "Base64 encode and decode routines by René Nyffenegger"
    license = "https://github.com/{0}/conan-{1}/blob/master/LICENSES".format(creator, name)
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "build_tests": [True, False]}
    default_options = {'shared': False, 'build_tests': False}
        
    def requirements(self):
        #use dynamic org/channel for libs in DEGoodmanWilson
        if self.options.build_tests:
            self.requires.add("gtest/1.8.0@bincrafters/stable", private=False)
            self.options["gtest"].shared = False

    def source(self):
        source_url = "https://github.com/{0}/{1}".format(self.creator, self.name)
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_BASE64_TESTS"] = self.options.build_tests
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
            self.copy(pattern="*.[h|hpp]", dst="include/{0}".format(self.name), src="sources")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
