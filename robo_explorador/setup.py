from setuptools import find_packages, setup

package_name = 'robo_explorador'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wilto',
    maintainer_email='wiltonjustinofilho@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publicador = robo_explorador.robo_topico_publish:main',
            'assinante = robo_explorador.robo_topico_subscriber:main',
            'servidor_coleta = robo_explorador.robo_coleta_servidor:main',
            'cliente_coleta = robo_explorador.robo_coleta_cliente:main',
            'servidor_acao = robo_explorador.robo_acao_servidor:main',
            'cliente_acao = robo_explorador.robo_acao_cliente:main',
            'cliente_acao_cancela = robo_explorador.robo_acao_cliente_cancela:main',
        ],
    },
)
