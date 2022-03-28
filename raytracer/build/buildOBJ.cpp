#include "../world/ViewPlane.hpp"
#include "../world/World.hpp"

#include "../utilities/RGBColor.hpp"
#include "../geometry/Geometry.hpp"
#include "../samplers/Sampler.hpp"
#include "../utilities/ShadeInfo.hpp"

#include "../cameras/Perspective.hpp"
#include "../cameras/Parallel.hpp"

#include "../geometry/Plane.hpp"
#include "../geometry/Sphere.hpp"

#include "../materials/Cosine.hpp"
#include "../materials/Matte.hpp"
#include "../materials/Reflective.hpp"

#include "../samplers/Simple.hpp"
#include "../samplers/Regular.hpp"

#include "../utilities/Constants.hpp"
#include "../utilities/Point3D.hpp"
#include "../light/Ambient.hpp"
#include "../light/Directional.hpp"
#include "../light/Point.hpp"
#include <ctime>
#include <iostream>

void World::build(void)
{

    // View plane  .
    vplane.top_left.x = -10;
    vplane.top_left.y = 10;
    vplane.top_left.z = 10;
    vplane.bottom_right.x = 10;
    vplane.bottom_right.y = -10;
    vplane.bottom_right.z = 10;
    vplane.hres = 800;
    vplane.vres = 800;

    // Background color.
    bg_color = black;

    // Camera and sampler.
    set_camera(new Perspective(0, 0, 20));
    // set_tracer(new whitted(this));
    set_tracer(new Basic(this));
    sampler_ptr = new Simple(camera_ptr, &vplane);

    // Custom Scene to tests times
    unsigned int rows = 40;
    unsigned int columns = 40;
    float radius = 2;
    Cosine *colors[] = {new Cosine(red), new Cosine(blue), new Cosine(white)};
    

    Reflective *ref_ptr1 = new Reflective;
    ref_ptr1->set_ka(0.75);
    ref_ptr1->set_kd(0.75);
    ref_ptr1->set_cd(static_cast<float>(rand()) / static_cast<float>(RAND_MAX), static_cast<float>(rand()) / static_cast<float>(RAND_MAX), static_cast<float>(rand()) / static_cast<float>(RAND_MAX));
    ref_ptr1->set_ks(0.1);
    ref_ptr1->set_exp(200.0);
    ref_ptr1->set_kr(1.0);

    Ambient *ambient_ptr = new Ambient;
    ambient_ptr->scale_radiance(0.2);
    set_ambient_light(ambient_ptr);

    //load mesh
    // addOBJ("tower of hanoi.obj", new Cosine(white));
    addOBJ("testmonke.obj", new Cosine(white));

    // builds the acceleration structure
    std::clock_t start;
    double duration;
    start = std::clock(); // get current time
    this->accelaration_ptr = new Octree(2, 8, this->geometry);
    duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;
    std::cout << "Octree build time: " << duration << "\n";
}
