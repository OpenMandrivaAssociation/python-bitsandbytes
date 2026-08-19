%undefine _debugsource_packages

# Same gfx list as python-torch's ROCm build.
%global rocm_arch gfx906;gfx908;gfx90a;gfx942;gfx1030;gfx1100;gfx1101;gfx1102;gfx1200;gfx1201

Name:		python-bitsandbytes
Version:	0.50.1
Release:	3
Summary:	k-bit optimizers and quantization
License:	MIT
Group:		Development/Python
URL:		https://github.com/bitsandbytes-foundation/bitsandbytes
Source0:	https://github.com/bitsandbytes-foundation/bitsandbytes/archive/refs/tags/%{version}.tar.gz#/bitsandbytes-%{version}.tar.gz
Patch0:		bitsandbytes-0.50.1-clang23-bf16-dot2.patch

BuildSystem:	python
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	clang
BuildRequires:	pkgconfig(python)
BuildRequires:	python
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(scikit-build-core)
BuildRequires:	python%{pyver}dist(numpy)
BuildRequires:	hipcc
# clang-linker-wrapper looks this up on PATH; hipcc only Requires clang.
BuildRequires:	/usr/bin/clang-offload-bundler
BuildRequires:	cmake(hip)
BuildRequires:	cmake(hipblas)
BuildRequires:	cmake(hiprand)
BuildRequires:	cmake(hipblaslt)
BuildRequires:	rocm-device-libs
Requires:	python%{pyver}dist(torch)
Requires:	python%{pyver}dist(numpy)
Requires:	python%{pyver}dist(packaging)

%description
8-bit / 4-bit quantization and optimizers for PyTorch (QLoRA, LLM.int8).
Ships both backends: CPU (no GPU / older cards) and HIP/ROCm (same gfx
targets as python-torch, any host arch). Runtime picks the HIP library
when torch sees a Radeon. No NVIDIA CUDA toolkit.

%build -p
export CC=clang
export CXX=clang++
export CMAKE_GENERATOR=Ninja
# CMake is one backend per configure. Build CPU first so machines
# without a current Radeon still have libbitsandbytes_cpu.so; the
# python/scikit-build pass then adds the HIP library next to it.
cmake -S . -B build-cpu \
	-DCOMPUTE_BACKEND=cpu \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_C_COMPILER=clang \
	-DCMAKE_CXX_COMPILER=clang++
cmake --build build-cpu --parallel
export ROCM_PATH=%{_prefix}
export HIP_CLANG_PATH=%{_bindir}
export HIP_DEVICE_LIB_PATH=%{_libdir}/amdgcn/bitcode
cat > hip-flags.cmake <<'EOF'
set(CMAKE_HIP_FLAGS "--rocm-path=%{_prefix} --rocm-device-lib-path=%{_libdir}/amdgcn/bitcode" CACHE STRING "" FORCE)
EOF
export CMAKE_ARGS="-C $PWD/hip-flags.cmake -DCOMPUTE_BACKEND=hip -DCMAKE_BUILD_TYPE=Release -DCMAKE_HIP_COMPILER=clang++ -DBNB_ROCM_ARCH=%{rocm_arch}"


%files
%doc README.md
%license LICENSE
%{python_sitearch}/bitsandbytes
%{python_sitearch}/bitsandbytes-*.*-info
