#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <tuple>
#include <vector>

namespace py = pybind11;

namespace fast_trimesh {
namespace cpu {
namespace trimesh {

template <typename T>
class Trimesh {
   private:
    std::vector<T> vertices;
    std::vector<std::tuple<int, int, int>> faces;

   public:
    Trimesh() = default;
    ~Trimesh() = default;

    // Accessor methods
    void add_vertex(T vertex) { vertices.push_back(vertex); }
    void add_face(int i, int j, int k) {
        faces.push_back(std::make_tuple(i, j, k));
    }
    std::vector<T> get_vertices() { return vertices; }
    std::vector<std::tuple<int, int, int>> get_faces() { return faces; }

    // Boolean operators
    Trimesh operator+(const Trimesh &other) {
        Trimesh result;
        result.vertices = vertices;
        result.faces = faces;
        auto offset = vertices.size();
        for (auto &face : other.faces) {
            result.faces.push_back(std::make_tuple(std::get<0>(face) + offset,
                                                   std::get<1>(face) + offset,
                                                   std::get<2>(face) + offset));
        }
        result.vertices.insert(result.vertices.end(), other.vertices.begin(),
                               other.vertices.end());

        return result;
    }

    Trimesh operator+=(const Trimesh &other) {
        auto offset = vertices.size();
        for (auto &face : other.faces) {
            faces.push_back(std::make_tuple(std::get<0>(face) + offset,
                                            std::get<1>(face) + offset,
                                            std::get<2>(face) + offset));
        }
        vertices.insert(vertices.end(), other.vertices.begin(),
                        other.vertices.end());
        return *this;
    }
};

void add_modules(py::module &m);

}  // namespace trimesh
}  // namespace cpu
}  // namespace fast_trimesh
