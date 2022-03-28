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
			sr.t = tmin;
			return (true);
		} 
	
		t = (-b + e) / denom;    // larger root
	
		if (t > kEpsilon) {
			tmin = t;
		sr.ray = ray;	
			sr.hit_point = ray.o + t * ray.d;
			sr.normal   = (temp + t * ray.d) / r;
			sr.normal.normalize();
			sr.t = tmin;
			return (true);
		} 
	}
	
	return (true);
}

bool Sphere::shadow_hit(const Ray& ray, float& t) const {
    Vector3D oc = ray.o - c;
    double _a = ray.d*ray.d;
    double _b = 2*oc*ray.d;
    double _c = (oc*oc) - (r*r);
    double discriminant = (_b*_b) - (4*_a*_c);

    if (discriminant < 0) {
        return false;
    }

    double e = std::sqrt(discriminant);
    double denom = 2*_a;
    double t0 = (-_b - e)/denom;

    if (t0 > kEpsilon) {
        t = t0;
        return true;
    }

    t0 = (-_b + e)/denom;
    if (t0 > kEpsilon) {
        t = t0;
        return true;
    }
    return false;
}
BBox Sphere::getBBox() const {
	Point3D p0(c.x - r, c.y - r, c.z - r);
	Point3D p1(c.x + r, c.y + r, c.z + r);
	return (BBox(p0, p1));
}
