"use strict";

let gl;  // WebGL "context"
let nt = 16; // Number of Iterations

window.onload = function init()
{
    
    let canvas = document.getElementById( "gl-canvas" );
    gl = canvas.getContext('webgl2');
    if (!gl) alert( "WebGL 2.0 isn't available" );

    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0 , 1.0, 1.0, 1.0 );
    
    //  Load shaders and initialize attribute buffers
    let program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );

    // Compute data.
    let vertices = [];
    let colors = []

    // Number of Pixels.
    var pixellen = canvas.height * canvas.width;

    for (var i = 0; i < canvas.height; i++)
    {
        // Mapping of each pixel to relevant point from -2 to 2, where mandelbrot occurs.
        var x = map_point(0, canvas.height, -2, 2, i);
        
        for (var j = 0; j < canvas.width; j++)
        {
            var y = map_point(0, canvas.width, -2, 2, j);

            // Our canvas only takes from -1 to 1, so we map each point previously mapped
            vertices.push(vec2(map_point(-2, 2, -1, 1, x), map_point(-2, 2, -1, 1, y)));

            // The value of c is the value from -2 to 2, in the complex plane
            var c = math.complex(x, y);
            // We start with z as 0+0i
            var z =  math.complex(0, 0);

            // Variable for holding escape time.
            var itercount = 0;
            var escaped = true;
            
            for (var k = 0; k < nt; k++)
            {
                // as per the formula given
                z = math.complex(z.re*z.re-z.im*z.im, 2*z.re*z.im);
                z = math.complex(z.re+c.re,  z.im+c.im);
                var v = math.sqrt(z.re*z.re+z.im*z.im);

                // If v is lesser than 2, it has not escaped yet.
                if (v <= 2)
                {
                    itercount += 1;
                }
            }
            if (v <= 2)
            {
                escaped = false;
            }

            // RGB color scheme, similar to picture in the assignment
            
            // if (escaped == false)
            // {
            //     colors.push(vec4(0.0, 0.0, map_point(0, nt, 0.5, 1.0, itercount), 1.0))
            // }
            // else
            // {
            //     colors.push(vec4(map_point(0, nt, 0.5, 0.0, itercount), itercount / nt, 0.0, 1.0))
            // }

            var r = 0.0, g = 0.0, b = 0.0;
            if (escaped == false)
            {
            b = 1.0 * (parseFloat(itercount)/parseFloat(nt));
            }
            else
            {
            r = 1.0* (parseFloat(itercount)/parseFloat(nt));
            }

            colors.push(vec4(r, parseFloat(itercount)/parseFloat(nt), b, 1.0));
            }
    }

    
    // Load the data into the GPU and bind to shader variables.
    gl.bindBuffer( gl.ARRAY_BUFFER, gl.createBuffer() );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW );
    
    // Associate out shader variables with our data buffer
    let vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 2, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer ());
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    let color = gl.getAttribLocation( program, "color" );
    gl.vertexAttribPointer( color, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( color );

    render(pixellen);
}

function render(pixellen) {
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.POINTS, 0, pixellen );
}

