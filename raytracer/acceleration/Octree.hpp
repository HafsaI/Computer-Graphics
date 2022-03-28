#pragma once

#include "Acceleration.hpp"
#include "OctreeNode.hpp"
#include "../utilities/ShadeInfo.hpp"

/**
 * 8 children space partition tree
 * 
 */
class Octree: public Acceleration {

    private: 
        // Maximun amount of objects to be hold by a single node of tree (when this limit is overflowed the node is subdivided)
        unsigned int maxObjectsPerChild;

        // Maximun depth of the tree (if reached the leaft will not be subdivided even if the max object allowed its overflowed)
        unsigned int maxDepthAllowed;

        // Root of the tree
        OctreeNode root;

        //Recursively finds the correct node to add the given geometry to the tree
        
        void addGeometry(OctreeNode &currentNode, unsigned int currentDepth, Geometry* geometry);

        // Checks if the geometry intersects any of the node's children and adds it to them
         
        void addToChildren(OctreeNode &currenNode, unsigned int currentDepth, Geometry *geometry);

        //Builds the childrens of the given node spreading its contained geometries ammong them
         
        void buildChildren(OctreeNode &currentNode, unsigned int currentDepth);

        //Recursively cast a ray through the nodes of the tree
         
        ShadeInfo castRay(const Ray &ray, const OctreeNode &currentNode, ShadeInfo &shadeInfo) const;

        //Cast a ray through the geometries contained by a leaf node
         
        ShadeInfo castLeaft(const Ray &ray, const OctreeNode &leaf, ShadeInfo &ShadeInfo) const;
    public:

        // Construct a new Octree object
    
        Octree(unsigned int maxObjectsPerChild, unsigned int maxDepthAllowed, std::vector<Geometry*> &scene);

       
        ShadeInfo hitObjects(const Ray &ray, ShadeInfo &shadeInfo) const;
        
        /**
         * Builds the Octree
         */
        void updateOctree();
};
