var renderWidth = $(window).width();
var renderHeight = $(window).height();
$('#notification').append('Resolution: ' + renderWidth);
$('#notification').append(' x ' + renderHeight);
$('#canvas').height(renderHeight);
$('#canvas').width(renderWidth);


var mouseLook = false;
$("#canvas").mousedown( function() { mouseLook = true; } );
$("#canvas").mouseup( function() { mouseLook = false; } );

var doc = new GLGE.Document();
var spotlight;
//GUI
function setShadowBias(newValue)
{
	document.getElementById("shadow_bias").innerHTML=newValue;
	spotlight.shadowBias = newValue;

}
function setSpotCosCutOff(newValue)
{
	document.getElementById("spot_cos_cut_off").innerHTML=newValue;
	spotlight.spotCosCutOff = newValue;
}
function setSpotExponent(newValue)
{
	document.getElementById("spot_exponent").innerHTML=newValue;
	spotlight.spotExponent = newValue;
}

doc.onLoad = function() {

	spotlight=doc.getElement("Lamp");
	// create the renderer
	var gameRenderer = new GLGE.Renderer(document.getElementById('canvas'));
	gameScene = new GLGE.Scene();
	gameScene = doc.getElement("Scene");
	gameRenderer.setScene(gameScene);
	var camera = gameScene.camera;
	camera.setAspect(renderWidth/renderHeight);

	//$('#notification').append('Renderer: '+ gameRenderer.canvas.width);
	//$('#notification').append(' x '+ gameRenderer.canvas.height);
	gameRenderer.canvas.height = renderHeight;
	gameRenderer.canvas.width = renderWidth;

	var mouse = new GLGE.MouseInput(document.getElementById('canvas'));
	var keys = new GLGE.KeyInput();
	var mouseovercanvas;
	var hoverobj;

	function mouselook() {
		if (mouseLook) {
			var mousepos = mouse.getMousePosition();

			mousepos.x = mousepos.x - document.body.offsetLeft;
			mousepos.y = mousepos.y	- document.body.offsetTop;
			
			var camera = gameScene.camera;
			camerarot = camera.getRotation();
			inc = (mousepos.y - (document.getElementById('canvas').offsetHeight / 2)) / 500;
			var trans=GLGE.mulMat4Vec4(camera.getRotMatrix(),[0,0,-1,1]);
			var mag=Math.pow(Math.pow(trans[0],2)+Math.pow(trans[1],2),0.5);
			trans[0]=trans[0]/mag;
			trans[1]=trans[1]/mag;
			camera.setRotX(1.56 - trans[1] * inc);
			camera.setRotZ(-trans[0] * inc);
			
			
			var width = document.getElementById('canvas').offsetWidth;
			if (mousepos.x < width * 0.3) {
				var turn = Math.pow((mousepos.x - width * 0.3) / (width * 0.3),
						2)
						* 0.005 * (now - lasttime);
				camera.setRotY(camerarot.y + turn);
			}
			if (mousepos.x > width * 0.7) {
				var turn = Math.pow((mousepos.x - width * 0.7) / (width * 0.3),
						2)
						* 0.005 * (now - lasttime);
				camera.setRotY(camerarot.y - turn);
			}
		}
	}

	function checkkeys(){
		var camera=gameScene.camera;
		camerapos=camera.getPosition();
		camerarot=camera.getRotation();
		var mat=camera.getRotMatrix();
		var trans=GLGE.mulMat4Vec4(mat,[0,0,-1,1]);
		var mag=Math.pow(Math.pow(trans[0],2)+Math.pow(trans[1],2),0.5);
		trans[0]=trans[0]/mag;
		trans[1]=trans[1]/mag;
		var yinc=0;
		var xinc=0;
		if(keys.isKeyPressed(GLGE.KI_M)) {addduck();}
		if(keys.isKeyPressed(GLGE.KI_W)) {yinc=yinc+parseFloat(trans[1]);xinc=xinc+parseFloat(trans[0]);}
		if(keys.isKeyPressed(GLGE.KI_S)) {yinc=yinc-parseFloat(trans[1]);xinc=xinc-parseFloat(trans[0]);}
		if(keys.isKeyPressed(GLGE.KI_A)) {yinc=yinc+parseFloat(trans[0]);xinc=xinc-parseFloat(trans[1]);}
		if(keys.isKeyPressed(GLGE.KI_D)) {yinc=yinc-parseFloat(trans[0]);xinc=xinc+parseFloat(trans[1]);}
		if(keys.isKeyPressed(GLGE.KI_LEFT_ARROW)) {camera.setRotZ(0.5);}
		if(levelmap.getHeightAt(camerapos.x+xinc,camerapos.y)>30) xinc=0;
		if(levelmap.getHeightAt(camerapos.x,camerapos.y+yinc)>30) yinc=0;
		if(levelmap.getHeightAt(camerapos.x+xinc,camerapos.y+yinc)>30){yinc=0;xinc=0;}
			else{
			camera.setLocZ(levelmap.getHeightAt(camerapos.x+xinc,camerapos.y+yinc)+8);
			}
		if(xinc!=0 || yinc!=0){
			camera.setLocY(camerapos.y+yinc*0.05*(now-lasttime));camera.setLocX(camerapos.x+xinc*0.05*(now-lasttime));
		}
	}

	levelmap = new GLGE.HeightMap("textures/map.png", 120, 120, -1500, 1500, -1500, 1500, 0, 150);

	var lasttime = 0;
	var frameratebuffer = 60;
	start = parseInt(new Date().getTime());
	var now;
	function render() {
		now = parseInt(new Date().getTime());
		frameratebuffer = Math
				.round(((frameratebuffer * 9) + 1000 / (now - lasttime)) / 10);
		document.getElementById("debug").innerHTML = "Frame Rate:"
				+ frameratebuffer;
		mouselook();
		checkkeys();
		gameRenderer.render();
		lasttime = now;
	}
	setInterval(render, 1);
	var inc = 0.2;
	document.getElementById("canvas").onmouseover = function(e) {
		mouseovercanvas = true;
	};
	document.getElementById("canvas").onmouseout = function(e) {
		mouseovercanvas = false;
	};
};
doc.load("meshes/nature.xml");
