#include "World.hpp"
#include <iostream>

World::World()
{
    vplane = ViewPlane();
    bg_color = RGBColor();

    camera_ptr = nullptr;
    sampler_ptr = nullptr;
}


World::~World()
{
    for (auto i: geometry)
    {
        delete i;
    }

    delete camera_ptr;
    delete sampler_ptr;
}

void World::add_geometry(Geometry *geom_ptr)
{
    this->geometry.push_back(geom_ptr);
}

void World::set_camera(Camera *c_ptr)
{
    this->camera_ptr = c_ptr;
}

ShadeInfo World::hit_objects(const Ray &ray)
{
    float max_t = kHugeValue;
    ShadeInfo hit_shade(*this);

    for (auto i: geometry)
    {
        float obj_tmin;
        ShadeInfo object_shade(*this);

        bool ray_intersection = i->hit(ray, obj_tmin, object_shade);

        if (ray_intersection && obj_tmin < max_t)
        {
            max_t = obj_tmin;
            //std::cout << object_shade.hit << "\n";
            object_shade.material_ptr = i->get_material();
            object_shade.hit = true;
            object_shade.t = obj_tmin;
            hit_shade = object_shade;
            
        }
    }

    return hit_shade;
}


void
World::build(void) {
  // View plane  .
  vplane.top_left.x = -10;
  vplane.top_left.y = 10;
  vplane.top_left.z = 10;
  vplane.bottom_right.x = 10;
  vplane.bottom_right.y = -10;
  vplane.bottom_right.z = 10;
  vplane.hres = 400;
  vplane.vres = 400;

  // Background color.  
  bg_color = black;
  
  // Camera and sampler.
  set_camera(new Perspective(0, 0, 20));
  sampler_ptr = new Simple(camera_ptr, &vplane);
	
  // sphere
  Sphere* sphere_ptr = new Sphere(Point3D(-3, 2, 0), 5); 
  sphere_ptr->set_material(new Cosine(red));
  add_geometry(sphere_ptr);
  
  // triangle
  Point3D a(2.5, -5, 1); 
  Point3D b(14, -1, 0); 
  Point3D c(8.5, 5, 0.5); 
  Triangle* triangle_ptr = new Triangle(a, b, c);
  triangle_ptr->set_material(new Cosine(blue));
  add_geometry(triangle_ptr);

  // plane
  Plane* plane_ptr = new Plane(Point3D(0,1,0), Vector3D(0, 10, 2)); 
  plane_ptr->set_material(new Cosine(green));  // green
  add_geometry(plane_ptr);
}