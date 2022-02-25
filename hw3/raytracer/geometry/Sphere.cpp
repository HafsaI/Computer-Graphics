#include "Sphere.hpp"
#include "math.h"
#include <sstream>
#include "../utilities/Constants.hpp"
#include "../utilities/Ray.hpp"
#include "../utilities/ShadeInfo.hpp"
#include "../utilities/BBox.hpp"

// maybe radius 0
Sphere::Sphere()	
	: 	Geometry(),
		c(0.0),
		r(1.0)
{}

Sphere::Sphere(const Point3D& c, float r): 	
        Geometry(),
		c(c),
		r(r)
{}

Sphere::Sphere (const Sphere& sphere)
	: 	Geometry(sphere),
		c(sphere.c),
		r(sphere.r)
{}

Sphere& Sphere::operator= (const Sphere& rhs)		
{
	if (this == &rhs)
		return (*this);

	Geometry::operator= (rhs);

	c = rhs.c;
	r= rhs.r;

	return (*this);
}

std::string Sphere::to_string() const {
    std::stringstream output;
    output << "center: (" << c.x << "," << c.y << "," << c.z << ")" << '\n';
    output << "radius: " << r;
    return output.str();
}

// checking if ray hits sphere
bool Sphere::hit(const Ray& ray, float& tmin, ShadeInfo& sr) const {
	double 		t;
	Vector3D	temp 	= ray.o - c;
	double 		a 		= ray.d * ray.d;
	double 		b 		= 2.0 * temp * ray.d;
	double 		c 	    = temp * temp - r * r;
	double 		disc	= b * b - 4.0 * a * c; // b2 - 4ac
	
	if (disc < 0.0) // no roots
		return(false);
	else {	
		double e = sqrt(disc);
		double denom = 2.0 * a;
		t = (-b - e) / denom;    // smaller root
	
		if (t > kEpsilon) {
			tmin = t;
					sr.ray = ray;
			sr.hit_point = ray.o + t * ray.d;
			sr.normal 	 = (temp + t * ray.d) / r;
			sr.normal.normalize();
			return (true);
		} 
	
		t = (-b + e) / denom;    // larger root
	
		if (t > kEpsilon) {
			tmin = t;
		sr.ray = ray;	
			sr.hit_point = ray.o + t * ray.d;
			sr.normal   = (temp + t * ray.d) / r;
			sr.normal.normalize();
			return (true);
		} 
	}
	
	return (true);
}

BBox Sphere::getBBox() const {
	Point3D p0(c.x - r, c.y - r, c.z - r);
	Point3D p1(c.x + r, c.y + r, c.z + r);
	return (BBox(p0, p1));
}
