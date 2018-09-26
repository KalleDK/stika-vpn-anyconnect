from setuptools import setup

setup(
    name='stika-vpn-anyconnect',
    version='0.0.13',
    packages=['stika.vpn.anyconnect', 'stika.vpn.anyconnect.event', 'stika.vpn.anyconnect.parser',
              'stika.vpn.anyconnect.vpncli'],
    package_dir={'': 'src'},
    url='https://github.com/KalleDK/stika-vpn-anyconnect',
    author='km',
    author_email='pip@k-moeller.dk',
    description='Wrapper for AnyConnect vpncli.exe',
    zip_safe=False,
    namespace_packages=['stika', 'stika.vpn'],
    install_requires=['typing-extensions'],
)
