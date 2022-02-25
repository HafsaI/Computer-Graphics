"use strict";

let gl;  // WebGL "context"
let score = 0;
let vertBuffer;
let colorBuffer;
let vertices = []
let canvas;
var clicked = false;
var interval = 3000;
var missed = 0;
var time;
var time2;


/* init() 

- Configures WebGL
- Reserves color and vertices buffers in GPU then binds to shader variables
- Calls render for rendering first polygon
- Calls updateScore() for updating score and rendering polygons continuously

*/
window.onload = function init()
{
    canvas = document.getElementById( "gl-canvas" );
    gl = canvas.getContext('webgl2');
    if (!gl) alert( "WebGL 2.0 isn't available" );
    
    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.0 , 0.0, 0.0, 1.0 );
    
    //  Load shaders and initialize attribute buffers
    let program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );

    vertBuffer = gl.createBuffer();
    colorBuffer = gl.createBuffer();

    // Load the data into the GPU and bind to shader variables.
    gl.bindBuffer( gl.ARRAY_BUFFER, vertBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, 6*8, gl.DYNAMIC_DRAW );

    // Associate shader attributes with corresponding data buffers
    let vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 2, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    // Load the data into the GPU and bind to shader variables.
    gl.bindBuffer( gl.ARRAY_BUFFER, colorBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, 12*8, gl.DYNAMIC_DRAW );
    
    // Associate shader attributes with corresponding data buffers
    let vColor = gl.getAttribLocation( program, "color" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    render();
    updateScore();
    
}

/* timer()

- Updates consec misses
- Calls render() for drawing new polygon

*/

function timer()
{

   // checks for triangle rendered before
    if (clicked == false) 
    {
        missed++;
    }
    render();
    
}

/* threeConsPoly()

- If no click for three consecutive polygons, score decremented
- If decremeted score is negative, gameover
*/

function threeConsPoly()
{

    // checks for three consec polygon misses
    if (missed == 3){
        score--;
        missed = 0;
        document.getElementById("score").innerHTML = score;
    
        // resets game if gameover
        if (score == -1)
        {
            clearInterval(time);
            clearInterval(time2);
            document.getElementById("score").innerHTML = score;
            alert("You LOST. Wait for few seconds after clicking OK so that the game can reset. ");
            gameOver();
            time = setInterval(timer,interval);
            time2 = setInterval(threeConsPoly, interval);
        }
    }
}


/* gameOver()

- initialises all game variables to initial values

*/

function gameOver()
{
    document.getElementById("score").innerHTML = score;
    vertices = [];
    gl.clearColor(0,0,0,1);
    score = 0;
    missed = 0;
    clicked = false;
}

/* updateScore()

- Calls timer() and threeCons Poly every 3 seconds
- Handles mouse click on canvas
- Calls render for rendering first polygon
- Calls updateScore() for updating score and rendering polygons continuously

*/
function updateScore(){
    if (score >= 0){
        // declaration of vars
        // calls timer and threeConsPoly every 3 sec
        time = setInterval(timer,interval);
        time2 = setInterval(threeConsPoly, interval);
        let x_Pos = 0.0;
        let y_Pos = 0.0;
        var hit;
        clicked = false;
        
        // handling click
        canvas.addEventListener('click', function(event) {

            clicked = true; // if clicked on canvas anywhere, polygon/blank space
            missed = 0;
            var midX = canvas.width/2;
            var midY = canvas.height/2;
            var rect = event.target.getBoundingClientRect();
            
            // -1 to +1
            x_Pos = ((event.clientX - rect.left) - midX) / midX;
            y_Pos = (midY - (event.clientY - rect.top)) / midY;
            // var to keep track of whether mouse click was on polygon
            hit = barycentric(vec2(x_Pos,y_Pos), vertices[0], vertices[1], vertices[2]); 

            if (score > -1) 
            {
                // clicked on the polygon
                if (hit)
                {
                    // increments score if clicked on polygon
                    score++; 
                    clearInterval(time);
                    clearInterval(time2);
                    // draws new polygon at new position
                    render(); 
                    time = setInterval(timer,interval);
                    time2 = setInterval(threeConsPoly, interval);
                    // updated incremented score
                    document.getElementById("score").innerHTML = score;
                    
                }
                // clicked on an empty space in canvas
                else
                {
                    // score decremented
                    score--;
                    document.getElementById("score").innerHTML = score;
                    // if score gets negative ie lost
                    if (score == -1)
                    {
                        document.getElementById("score").innerHTML = score;
                        clearInterval(time);
                        clearInterval(time2);
                        alert("You LOST. Wait for few seconds after clicking OK so that the game can reset. ");
                        // calls gameover() to reset the game
                        gameOver();
                        time = setInterval(timer,interval);
                        time2 = setInterval(threeConsPoly, interval);
                        
                        

                    }
                }
            }
        });


    }
}


/* render()

- finds new random position for polygon to be rendered
- draws the new polygon on canvas

*/  
function render() {
    clicked = false; // not yet clicked for new triangle that will be rendered
    // displays score
    document.getElementById("score").innerHTML = score;
    gl.clear( gl.COLOR_BUFFER_BIT );

    // specifying random positions for polygons
    let randpointx = map_point(0, 1, -0.8, 0.8, Math.random());
    let randpointy = map_point(0, 1, -0.8, 0.8, Math.random());
    
    // new Polygons positions and colors assigned to vertices and colors arrays
    vertices = [vec2(randpointx-0.2, randpointy-0.2), vec2(randpointx, randpointy+0.2), vec2(randpointx+0.2, randpointy-0.2)];
    let colors = [vec4(Math.random(), Math.random(), 0.0, 1.0), vec4(0.0, Math.random(), Math.random(), 1.0), vec4(Math.random(), 0.0, Math.random(), 1.0)];

    // Update webgl vertex buffer so that updated indices data is rendered
    gl.bindBuffer(gl.ARRAY_BUFFER, vertBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);
    
    gl.drawArrays( gl.TRIANGLES, 0, 3 );

}


// SOURCE: https://gamedev.stackexchange.com/questions/23743/whats-the-most-efficient-way-to-find-barycentric-coordinates
// It is using cramer's rule to solve ' p = p0 + (p1 - p0) * s + (p2 - p0) * t ' esentially, 
// and returns True if coefficients can add up to 1, as well as each individual coefficient being positive.

function barycentric(p, a, b, c)
{   
    var u=0.0, v=0.0, w=0.0;
    var v0 = subtract(b, a);
    var v1 = subtract(c, a);
    var v2 = subtract(p, a);
    var d00 = dot(v0, v0);
    var d01 = dot(v0, v1);
    var d11 = dot(v1, v1);
    var d20 = dot(v2, v0);
    var d21 = dot(v2, v1);
    var denom = d00 * d11 - d01 * d01;
    v = (d11 * d20 - d01 * d21) / denom;
    w = (d00 * d21 - d01 * d20) / denom;
    u = 1.0 - v - w;
    return (u + v + w == 1.0 && u > 0 && v > 0 && w > 0);
}

