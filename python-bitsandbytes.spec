%undefine _debugsource_packages

# CPU backend: AVX2/NEON kernels, no CUDA/HIP. Works on every arch.
# A HIP/RDNA rebuild is blocked today by rocprim (warp 32 vs wave 64)
# and clang 23 bf16 vector types in the 4-bit GEMM.
Name:		python-bitsandbytes
Version:	0.50.1
Release:	1
Summary:	k-bit optimizers and quantization (CPU)
License:	MIT
Group:		Development/Python
URL:		https://github.com/bitsandbytes-foundation/bitsandbytes
Source0:	https://github.com/bitsandbytes-foundation/bitsandbytes/archive/refs/tags/%{version}.tar.gz#/bitsandbytes-%{version}.tar.gz

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
Requires:	python%{pyver}dist(torch)
Requires:	python%{pyver}dist(numpy)
Requires:	python%{pyver}dist(packaging)

%description
8-bit / 4-bit quantization and optimizers for PyTorch (QLoRA, LLM.int8).
Built for CPU (AVX2 on x86_64, portable kernels on aarch64) so the same
source RPM is hardware-independent. No NVIDIA CUDA toolkit is required.
A ROCm/HIP variant can be added once upstream kernels compile with
clang 23 and mixed wave32/wave64 targets.

%prep -a

%build -p
export CC=clang
export CXX=clang++
export CMAKE_GENERATOR=Ninja
export CMAKE_ARGS="-DCOMPUTE_BACKEND=cpu -DCMAKE_BUILD_TYPE=Release"

%files
%doc README.md
%license LICENSE
%{python_sitearch}/bitsandbytes
%{python_sitearch}/bitsandbytes-*.*-info
