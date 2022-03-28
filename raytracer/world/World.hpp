#pragma once

/**
   This file declares the World class which contains all the information about
   the scene - geometry and materials, lights, viewplane, camera, samplers, and
   acceleration structures.

   It also traces rays through the scene.

   Courtesy Kevin Suffern.
*/

#include <vector>

#include "ViewPlane.hpp"

#include "../utilities/RGBColor.hpp"
#include "../geometry/Geometry.hpp"
#include "../samplers/Sampler.hpp"
#include "../utilities/ShadeInfo.hpp"

#include "../cameras/Perspective.hpp"
#include "../cameras/Parallel.hpp"

#include "../geometry/Plane.hpp"
#include "../geometry/Sphere.hpp"
#include "../geometry/Triangle.hpp"

#include "../materials/Cosine.hpp"

#include "../samplers/Simple.hpp"

#include "../utilities/Constants.hpp"
#include "../light/Ambient.hpp"
#include "../light/Directional.hpp"
#include "../light/Point.hpp"

#include "../acceleration/Acceleration.hpp"
#include "../acceleration/Octree.hpp"

#include "../tracer/Basic.hpp"
#include "../tracer/whitted.hpp"

class Camera;
class Geometry;
class Ray;
class Sampler;
class ShadeInfo;
class Light;
class Tracer;

class World
{

private:
  ShadeInfo regular_hit_objects(const Ray &ray);
  ShadeInfo accelerated_hit_objects(const Ray &ray);

public:
  ViewPlane vplane;
  RGBColor bg_color;
  std::vector<Geometry *> geometry;
  std::vector<Light *> lights;
  Light *ambient_ptr;
  Camera *camera_ptr;
  Sampler *sampler_ptr;
  Acceleration *accelaration_ptr;
  Tracer *tracer_ptr;

public:
  // Constructors.
  World(); // initialize members.

  // Destructor.
  ~World(); // free memory.

  // Add to the scene.
  void add_geometry(Geometry *geom_ptr);
  void add_light(Light *light_ptr);
  void set_camera(Camera *c_ptr);
  void set_ambient_light(Ambient *amb_ptr);
  void set_tracer(Tracer *t_ptr);
  // Build scene - add all geometry, materials, lights, viewplane, camera,
  // samplers, and acceleration structures
  void build();
  void addOBJ(const char *path, Material *mPtr);
  // Returns appropriate shading information corresponding to intersection of
  // the ray with the scene geometry.
  ShadeInfo hit_objects(const Ray &ray, bool accelerate = true);
};
