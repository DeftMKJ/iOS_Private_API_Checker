import subprocess
import re
"""
针对目标文件的展示工具，用来发现应用中使用到了哪些系统库，
调用了其中哪些方法，使用了库中哪些对象及属性，它是Xcode自带的常用工具。下面是一些常用的命令：
-f print the fat headers
-a print the archive header
-h print the mach header
-l print the load commands
-L print shared libraries used
-D print shared library id name
-t print the text section (disassemble with -v)
-p <routine name>  start dissassemble from routine name
-s <segname> <sectname> print contents of section
-d print the data section
-o print the Objective-C segment
-r print the relocation entries
-S print the table of contents of a library
-T print the table of contents of a dynamic shared library
-M print the module table of a dynamic shared library
-R print the reference table of a dynamic shared library
-I print the indirect symbol table
-H print the two-level hints table
-G print the data in code table
-v print verbosely (symbolically) when possible
-V print disassembled operands symbolically
-c print argument strings of a core file
-X print no leading addresses or headers
-m don't use archive(member) syntax
-B force Thumb disassembly (ARM objects only)
-q use llvm's disassembler (the default)
-Q use otool(1)'s disassembler
-mcpu=arg use `arg' as the cpu for disassembly
-j print opcode bytes
-P print the info plist section as strings
-C print linker optimization hints
--version print the version of /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/otool
"""


otool_path = '/usr/bin/otool' # otool 所在位子

otool_cms = otool_path + " -L %s"

def otool_app(app):
    """
    获取app中遇到的framework
    -L print shared libraries used
    app: Mach-O path
    """

    cmd = otool_cms % app

    out = subprocess.check_output(cmd.split()).decode('utf-8')

    private = set()
    public = set()

    pub_pattern = re.compile(r"Frameworks/([.\w]*)")
    pri_pattern = re.compile(r"PrivateFrameworks/(\w*).framework")

    for line in re.finditer(pub_pattern, out):
        public.add(line.groups()[0])

    for line in re.finditer(pri_pattern, out):
        private.add(line.groups()[0])

    print(private)
    print(public)

    return private, public




if __name__ == '__main__':
    path = '/Users/mikejing191/Desktop/T2/Payload/SmartPay_Example.app/SmartPay_Example'
    out_put =  otool_app(path)
    # print(out_put)

    """
    /Users/mikejing191/Desktop/iOS_Private_API_Checker/venv/bin/python /Users/mikejing191/Desktop/iOS_Private_API_Checker/dump/otool_utils.py
/Users/mikejing191/Desktop/T2/Payload/SmartPay_Example.app/SmartPay_Example (architecture armv7):
	/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation (compatibility version 150.0.0, current version 1560.10.0)
	@rpath/FCUUID.framework/FCUUID (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/Foundation.framework/Foundation (compatibility version 300.0.0, current version 1560.10.0)
	/System/Library/Frameworks/ImageIO.framework/ImageIO (compatibility version 1.0.0, current version 0.0.0)
	@rpath/MJRefresh.framework/MJRefresh (compatibility version 1.0.0, current version 1.0.0)
	@rpath/Masonry.framework/Masonry (compatibility version 1.0.0, current version 1.0.0)
	@rpath/SDWebImage.framework/SDWebImage (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/Security.framework/Security (compatibility version 1.0.0, current version 58286.222.2)
	@rpath/UICKeyChainStore.framework/UICKeyChainStore (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/UIKit.framework/UIKit (compatibility version 1.0.0, current version 61000.0.0)
	@rpath/YYModel.framework/YYModel (compatibility version 1.0.0, current version 1.0.0)
	/usr/lib/libicucore.A.dylib (compatibility version 1.0.0, current version 62.1.0)
	/System/Library/Frameworks/CoreLocation.framework/CoreLocation (compatibility version 1.0.0, current version 2245.8.12)
	/System/Library/Frameworks/AdSupport.framework/AdSupport (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/Photos.framework/Photos (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/MobileCoreServices.framework/MobileCoreServices (compatibility version 1.0.0, current version 935.2.0)
	/System/Library/Frameworks/CoreMedia.framework/CoreMedia (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/AudioToolbox.framework/AudioToolbox (compatibility version 1.0.0, current version 492.0.0)
	/System/Library/Frameworks/AVFoundation.framework/AVFoundation (compatibility version 1.0.0, current version 2.0.0)
	/System/Library/Frameworks/CFNetwork.framework/CFNetwork (compatibility version 1.0.0, current version 975.0.3)
	/System/Library/Frameworks/SystemConfiguration.framework/SystemConfiguration (compatibility version 1.0.0, current version 963.200.27)
	/System/Library/Frameworks/CoreTelephony.framework/CoreTelephony (compatibility version 1.0.0, current version 0.0.0)
	/usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 400.9.4)
	/usr/lib/libsqlite3.dylib (compatibility version 9.0.0, current version 274.20.0)
	/usr/lib/libz.1.dylib (compatibility version 1.0.0, current version 1.2.11)
	/usr/lib/libobjc.A.dylib (compatibility version 1.0.0, current version 228.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1252.200.5)
	/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics (compatibility version 64.0.0, current version 1245.9.2)
	/System/Library/Frameworks/CoreImage.framework/CoreImage (compatibility version 1.0.0, current version 5.0.0)
	/System/Library/Frameworks/CoreText.framework/CoreText (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/QuartzCore.framework/QuartzCore (compatibility version 1.2.0, current version 1.11.0)
	/System/Library/Frameworks/WebKit.framework/WebKit (compatibility version 1.0.0, current version 606.2.104)
/Users/mikejing191/Desktop/T2/Payload/SmartPay_Example.app/SmartPay_Example (architecture arm64):
	/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation (compatibility version 150.0.0, current version 1560.10.0)
	@rpath/FCUUID.framework/FCUUID (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/Foundation.framework/Foundation (compatibility version 300.0.0, current version 1560.10.0)
	/System/Library/Frameworks/ImageIO.framework/ImageIO (compatibility version 1.0.0, current version 0.0.0)
	@rpath/MJRefresh.framework/MJRefresh (compatibility version 1.0.0, current version 1.0.0)
	@rpath/Masonry.framework/Masonry (compatibility version 1.0.0, current version 1.0.0)
	@rpath/SDWebImage.framework/SDWebImage (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/Security.framework/Security (compatibility version 1.0.0, current version 58286.222.2)
	@rpath/UICKeyChainStore.framework/UICKeyChainStore (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/UIKit.framework/UIKit (compatibility version 1.0.0, current version 61000.0.0)
	@rpath/YYModel.framework/YYModel (compatibility version 1.0.0, current version 1.0.0)
	/usr/lib/libicucore.A.dylib (compatibility version 1.0.0, current version 62.1.0)
	/System/Library/Frameworks/CoreLocation.framework/CoreLocation (compatibility version 1.0.0, current version 2245.8.12)
	/System/Library/Frameworks/AdSupport.framework/AdSupport (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/Photos.framework/Photos (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/MobileCoreServices.framework/MobileCoreServices (compatibility version 1.0.0, current version 935.2.0)
	/System/Library/Frameworks/CoreMedia.framework/CoreMedia (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/AudioToolbox.framework/AudioToolbox (compatibility version 1.0.0, current version 492.0.0)
	/System/Library/Frameworks/AVFoundation.framework/AVFoundation (compatibility version 1.0.0, current version 2.0.0)
	/System/Library/Frameworks/CFNetwork.framework/CFNetwork (compatibility version 1.0.0, current version 975.0.3)
	/System/Library/Frameworks/SystemConfiguration.framework/SystemConfiguration (compatibility version 1.0.0, current version 963.200.27)
	/System/Library/Frameworks/CoreTelephony.framework/CoreTelephony (compatibility version 1.0.0, current version 0.0.0)
	/usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 400.9.4)
	/usr/lib/libsqlite3.dylib (compatibility version 9.0.0, current version 274.20.0)
	/usr/lib/libz.1.dylib (compatibility version 1.0.0, current version 1.2.11)
	/usr/lib/libobjc.A.dylib (compatibility version 1.0.0, current version 228.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1252.200.5)
	/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics (compatibility version 64.0.0, current version 1245.9.2)
	/System/Library/Frameworks/CoreImage.framework/CoreImage (compatibility version 1.0.0, current version 5.0.0)
	/System/Library/Frameworks/CoreText.framework/CoreText (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/QuartzCore.framework/QuartzCore (compatibility version 1.2.0, current version 1.11.0)
	/System/Library/Frameworks/WebKit.framework/WebKit (compatibility version 1.0.0, current version 606.2.104)
    """