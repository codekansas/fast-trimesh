#include "io.h"

using namespace pybind11::literals;

namespace fast_trimesh {
namespace cpu {
namespace io {

void save_stl(const std::string &filename, const trimesh::Trimesh3D &mesh) {}

void add_modules(py::module &m) {
    // Defines a new submodule.
    auto io = m.def_submodule("io");

    m.def("save_stl", &save_stl, "Saves a mesh to an STL file", "filename"_a,
          "mesh"_a);
}

}  // namespace io
}  // namespace cpu
}  // namespace fast_trimesh
