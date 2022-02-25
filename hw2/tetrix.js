"use strict";

var canvas; var gl; var positions = []; var colors = []; var recursions = 0;
var xAxis = 0; var yAxis = 1; var zAxis = 2; var axis = 1; var theta = [0, 0, 0];
var flag = true; var thetaLoc; var cBuffer; var vBuffer;


/* init() 

- Configures WebGL
- Handles button click events (for switching axis of rotation of tetrahedron)
- Gets level of recursion from slider 
- Reserves color and vertices buffers in GPU then binds to shader variables
- Calls render for rendering sierpinski on canvas

*/

window.onload = function init()
{
    canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");

    
    //  Configure WebGL
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0, 0, 0, 1.0);

    // enable hidden-surface removal
    gl.enable(gl.DEPTH_TEST);
   
    //  Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    // Created buffer objects, initialized it, and associate it with the
    // associated attribute variable in our vertex shader
    cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER,  8*Math.pow(3,10), gl.DYNAMIC_DRAW);

    var colorLoc = gl.getAttribLocation(program, "aColor");
    gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(colorLoc);

    vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, 8*Math.pow(3,10), gl.DYNAMIC_DRAW);

    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    // for rotation angle
    thetaLoc = gl.getUniformLocation(program, "uTheta");



    //event listeners for buttons
    document.getElementById( "xButton" ).onclick = function () {
        axis = xAxis;
    };
    document.getElementById( "yButton" ).onclick = function () {
        axis = yAxis;
    };
    document.getElementById( "zButton" ).onclick = function () {
        axis = zAxis;
    };
    document.getElementById("ButtonToggle").onclick = function(){
        flag = !flag;
    };
    document.getElementById("slider").onchange = function(event) {
        recursions = parseInt(event.target.value);
        
    };

    render();
};

/* triangle() 

- pushes colors and positions into their respective array 
  of each divided triangle side of tetrahedron

*/
function triangle( a, b, c, color )
{
    // add colors and vertices for each tetrahedron
    // bonus
    var baseColors = [
        vec4(0.952,0.556,0.447,1), // orange
        vec4(0.427, 0.348, 0.478,1), //purple
        vec4(0.612,0.671,0.698,1), // lightblue
        vec4(0.137,0.20,0.259,1) //dark blue
    ];

    colors.push(baseColors[color]);
    positions.push(a);
    colors.push(baseColors[color]);
    positions.push(b);
    colors.push(baseColors[color]);
    positions.push(c);
}


/* tetra() 

- calls triangle() to push vertices into arrays for each face of tetrahedron

*/
function tetra( a, b, c, d )
{
    // tetrahedron with each side using
    // a different color

    triangle(a, c, b, 0);
    triangle(a, c, d, 1);
    triangle(a, b, d, 2);
    triangle(b, c, d, 3);
}

/* sierpinskiTetra() 

- divides each face of tetrahedron 
  to get to the recursion level specified

*/
function sierpinskiTetra(a, b, c, d, count)
{
    // base case
    if (count === 0) {
        tetra(a, b, c, d);
    }

    else {
        // midpoints of sides
        var ab = mix(a, b, 0.5);
        var ac = mix(a, c, 0.5);
        var ad = mix(a, d, 0.5);
        var bc = mix(b, c, 0.5);
        var bd = mix(b, d, 0.5);
        var cd = mix(c, d, 0.5);

        --count;
        // divide four smaller tetrahedrons
        sierpinskiTetra(a, ab, ac, ad, count);
        sierpinskiTetra(ab,  b, bc, bd, count);
        sierpinskiTetra(ac, bc,  c, cd, count);
        sierpinskiTetra(ad, bd, cd,  d, count);
    }
}


/* render() 

- initialized tetrahedron vertices
- calls func sierpinskiTetra to make sierpinski tetrahedron acc to recursion step
- uses gl.bufferData to pass positions and colors array to GPU
- takes care of rotation of tetrahedron
- renders tetrahedron

*/

function render() {

    // tetrahedron vertices
    var vertices = [
        vec4(0.0000,  0.0000, -1.0000,1.0),
        vec4(0.0000,  0.9428,  0.3333,1.0),
        vec4(-0.8165, -0.4714,  0.3333,1.0),
        vec4(0.8165, -0.4714,  0.3333,1.0)
    ];
    positions = [];
    colors = [];

    // calling function for making sierpinski tetrahedron with the level of recursion specified by user
    sierpinskiTetra(vertices[0], vertices[1], vertices[2], vertices[3],
        recursions);

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.DYNAMIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.DYNAMIC_DRAW);


    // taking care of rotation of tetrahedron
    if(flag) theta[axis] += 2.0;
    gl.uniform3fv(thetaLoc, theta);
    gl.drawArrays( gl.TRIANGLES, 0, positions.length );
   
    positions = [];
    colors = [];
    requestAnimationFrame(render);

}
