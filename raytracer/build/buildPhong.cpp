/**
   This builds a simple scene that consists of a sphere, and a
   plane and a box. 
   Perspective viewing is used with a single sample per pixel.
   Ambient and Diffuse Shading - a ray-cast tracer
*/

#include "../cameras/Perspective.hpp"

#include "../geometry/Plane.hpp"
#include "../geometry/Sphere.hpp"
#include "../geometry/Triangle.hpp"
#include "../geometry/Box.hpp"


#include "../materials/Cosine.hpp"
#include "../materials/Matte.hpp"


#include "../samplers/Simple.hpp"
#include "../samplers/Regular.hpp"

#include "../utilities/Constants.hpp"

#include "../light/Ambient.hpp"
#include "../light/Directional.hpp"
#include "../light/Point.hpp"
#include "../light/Spotlight.hpp"


#include "../tracer/Basic.hpp"
#include "../world/World.hpp"




//Phong

void 												
World::build(void) {
	// View plane  .
    vplane.top_left.x = -4;
    vplane.top_left.y = 6;
    vplane.top_left.z = 2;
    vplane.bottom_right.x = 10;
    vplane.bottom_right.y = -0.5;
    vplane.bottom_right.z = 2;
    vplane.hres = 600;
    vplane.vres = 400;

    
	bg_color = black;
    
    // Camera and sampler.
	set_camera(new Perspective(2, 2.5, 15));
    set_tracer(new Basic(this));
    sampler_ptr = new Simple(camera_ptr, &vplane);
			
	// Ambient* ambient_ptr = new Ambient;
	// ambient_ptr->scale_radiance(0.5);
	// set_ambient_light(ambient_ptr);
	
	
	Directional* light_ptr1 = new Directional();
    light_ptr1->set_direction(-12, 15, 30); 
	light_ptr1->scale_radiance(2.0);
	//light_ptr1->set_shadows(true);				
	add_light(light_ptr1);
		
	Point* light_ptr2 = new Point();
	light_ptr2->set_position(-12, 15, 30); 
	light_ptr2->scale_radiance(2.0);
	//light_ptr2->set_shadows(true);				
	add_light(light_ptr2);
		
	// sphere
	
	Phong* phong_ptr1 = new Phong;			
	phong_ptr1->set_ka(0.25); 
	phong_ptr1->set_kd(0.75);
	phong_ptr1->set_cd(0.5, 0.6, 0);  	// dark yellow
	phong_ptr1->set_ks(0.25);
	phong_ptr1->set_exp(50);
	
	Sphere*	sphere_ptr1 = new Sphere(Point3D(0.0, 2.4, 0), 1.5); 
	sphere_ptr1->set_material(phong_ptr1);
	add_geometry(sphere_ptr1);	
	
	// box
	
	Phong* phong_ptr3 = new Phong;			
	phong_ptr3->set_ka(0.4); 
	phong_ptr3->set_kd(0.75);
	phong_ptr3->set_cd(0.8,0.5,0);			// orange
	phong_ptr3->set_ks(0.25);
	phong_ptr3->set_exp(4);
							
	Box* box_ptr1 = new Box(Point3D(5.4, -0.5, -3), Point3D(7.5, 4.75, 0.60));
	box_ptr1->set_material(phong_ptr3);
	add_geometry(box_ptr1);
		
	// triangle
	
	Phong* phong_ptr4 = new Phong;			
	phong_ptr4->set_ka(0.35); 
	phong_ptr4->set_kd(0.5);
	phong_ptr4->set_cd(0, 0.5, 0.5);   	// cyan
	phong_ptr4->set_ks(0.5);
	phong_ptr4->set_exp(3);

	Triangle* triangle_ptr1 = new Triangle(	Point3D(1.5, -0.5, 1.8), 		// front
											Point3D(7.5, -0.5, -9.00), 		// back
											Point3D(2.35, 5.8, 1.4));		// top									
	triangle_ptr1->set_material(phong_ptr4);        
	add_geometry(triangle_ptr1);
		

	// ground plane

	Matte* matte_ptr4 = new Matte();			
	matte_ptr4->set_ka(0.1); 
	matte_ptr4->set_kd(0.2);
	matte_ptr4->set_cd(white);
	
	Plane* plane_ptr = new Plane(Point3D(0, -0.5, 0), Vector3D(0, 1, 0));
	plane_ptr->set_material(matte_ptr4);
	add_geometry(plane_ptr);
}