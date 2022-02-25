"use strict";

let gl; var positions= []; var trianglemode = true; var triangles = []; var quads = [];
var extra = []; var tcolors = []; var qcolors = []; var colors = [];

/* init() 

- Configures WebGL
- Handles key events (for resetting and toggling between modes)
- Handles mouse events (for vertices specified by mouse clicks )
- Reserves color and vertices buffers in GPU then binds to shader variables
- Handles key/mouse events
- Calls render for rendering shapes on canvas

*/

window.onload = function init()
{
    let canvas = document.getElementById( "gl-canvas" );
    gl = canvas.getContext('webgl2');
    if (!gl) alert( "WebGL 2.0 isn't available" );

    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    //  Black colour 
    gl.clearColor(0, 0, 0, 1.0);

    
    //  Load shaders and initialize attribute buffers
    let program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );


    // Load the data into the GPU and bind to shader variables.
    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, 10*Math.pow(3,10), gl.DYNAMIC_DRAW);

   
    // Associate shader attributes with corresponding data buffers
    let vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 3, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    // Load the data into the GPU and bind to shader variables.
    var cBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, 10*Math.pow(3,10), gl.DYNAMIC_DRAW );
 
    
    // Associate shader attributes with corresponding data buffers
    let colorLoc = gl.getAttribLocation( program, "aColor" );
    gl.vertexAttribPointer( colorLoc, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( colorLoc );


    //handling key events
    document.addEventListener('keydown', (event) => {
        var name = event.key;
        // clears canvas
        if (name == 'r' || name ==  'R'){
            positions = [];
            triangles = [];
            quads = [];
            tcolors = [];
            qcolors = [];
            colors = [];
            extra = [];
            trianglemode = true;
            document.getElementById("mode").innerHTML = "Triangle Mode";
            
        }
        // toggles between tri & quad mode if keypress = t/T
        else if (name == 't' || name ==  'T'){
       
            //turns to quad mode
            if (trianglemode == true){
                trianglemode = !trianglemode; 
                document.getElementById("mode").innerHTML = "Quadrilateral Mode";

            }
            //turns to tri mode
            else if (trianglemode == false){ 

                trianglemode = !trianglemode; 
                if (extra.length == 3){
                    var r = Math.random();
                    var g = Math.random();
                    var b = Math.random();
                    for ( var i = 0; i < extra.length; ++i ) {
                        triangles.push(extra[i]);
                        tcolors.push(vec4(r,g,b,1));
                    }
                    extra = [];
                }
                document.getElementById("mode").innerHTML = "Triangle Mode";

            }
           
        }
        render(vBuffer, cBuffer);
    });


    // handles mouse click on canvas
    canvas.addEventListener("click", function(event)
    {
        var rect = event.target.getBoundingClientRect();
        var x = event.clientX;
        var y = event.clientY;
        
        var midX = canvas.width/2;
        var midY = canvas.height/2;

        // converting canvas coordinate between -1 to +1
        x = ((x - rect.left) - midX) / midX;
        y = (midY - (y - rect.top)) / midY;

        // push triangle vertices 
        if (trianglemode == true) {
            extra.push(vec3(x,y,0.0));
            // if three points drawn, then push to triangle array for drawing
            if (extra.length == 3){
                // random color being generated for triangles
                var r = Math.random();
                var g = Math.random();
                var b = Math.random();
                for ( var i = 0; i < extra.length; ++i ) {
                    triangles.push(extra[i]);
                    tcolors.push(vec4(r,g,b,1));
                    
                   
                }
                extra = [];
            }
        }
        // push quad vertices 
        else{
            extra.push(vec3(x,y,0.0));
            // if four points are drawn, then push to quad array for drawing
            if (extra.length == 4){
                // random color being generated for quadrilateral
                var r = Math.random();
                var g = Math.random();
                var b = Math.random();
                var indices = [3,2,1,3,1,0];
                for ( var i = 0; i < indices.length; ++i ) {
                    quads.push(extra[indices[i]]);
                    qcolors.push(vec4(r,g,b,1));
                    
                }
                extra = [];
            }
        }
        
        render(vBuffer, cBuffer);
    });
 
    
    render(vBuffer, cBuffer);
}


/* render(vBuffer,cBuffer)

 - Takes vertices buffer and color buffer as arguments to pass data into GPU
 - Creates and appends vertices and colors of all shapes drawn to their respective arrays
 - Draws triangles and quadrilaterals
 - Draws vertices that are not yet completed polygons

*/
function render(vBuffer, cBuffer) {
   
    gl.clear( gl.COLOR_BUFFER_BIT );

    // merging triangles and quadrilaterals vertices + colors 
    // and appending them to positions and colors arrays
    
    if (triangles.length != 0){
        positions.push.apply(positions, triangles.slice(0,triangles.length));
        colors.push.apply(colors, tcolors.slice(0,tcolors.length));
    }

    if (quads.length != 0){
        positions.push.apply(positions, quads.slice(0,quads.length));
        colors.push.apply(colors, qcolors.slice(0,qcolors.length));
    }
    
    // drawing all shapes
    if (positions.length != 0){
        // loading colors and positions of shapes to buffers
        gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
        gl.bufferData( gl.ARRAY_BUFFER, flatten(colors), gl.DYNAMIC_DRAW  );
        gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
        gl.bufferData( gl.ARRAY_BUFFER, flatten(positions), gl.DYNAMIC_DRAW );
        gl.drawArrays( gl.TRIANGLES, 0, positions.length );
    }
    

    positions = [];
    colors = [];

    // for vertices that are not yet completed polygons
    positions.push.apply(positions,extra.slice(0,extra.length));

    // pushing white color for single vertices
    for ( var i = 0; i < extra.length; ++i ) {
        colors.push(vec4(1,1,1,1));
    }
    if (positions.length != 0){
        // loading colors and positions of vertices to buffers
        gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
        gl.bufferData( gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW );
        gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
        gl.bufferData( gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW );
        // drawing dots
        gl.drawArrays( gl.POINTS, 0, positions.length );
    }
    positions = [];
    colors = [];
    
}
    