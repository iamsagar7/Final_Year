// // console.clear();
// // var renderer = new THREE.WebGLRenderer({
// //   canvas: document.querySelector("canvas"),
// //   antialias: true
// // });
// // renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1);
// // renderer.setSize(window.innerWidth, window.innerHeight);
// // var scene = new THREE.Scene();
// // var camera = new THREE.PerspectiveCamera(
// //   45,
// //   window.innerWidth / window.innerHeight,
// //   1,
// //   1000
// // );
// // camera.position.z = 60;
// // var length = 30;
// // var mouseJump = {
// //   x: 0,
// //   y: 0
// // };
// // var offset = 0;

// // function Spline() {
// //   this.geometry = new THREE.Geometry();
// //   this.color = Math.floor(Math.random() * 80 + 180);
// //   for (var j = 0; j < 180; j++) {
// //     this.geometry.vertices.push(
// //       new THREE.Vector3(j / 180 * length * 2 - length, 0, 0)
// //     );
// //     this.geometry.colors[j] = new THREE.Color(
// //       "hsl(" + (j * 0.6 + this.color) + ",70%,70%)"
// //     );
// //   }
// //   this.material = new THREE.LineBasicMaterial({
// //     vertexColors: THREE.VertexColors
// //   });
// //   this.mesh = new THREE.Line(this.geometry, this.material);
// //   this.speed = (Math.random() + 0.1) * 0.0002;
// //   scene.add(this.mesh);
// // }
// // var isMouseDown = false;
// // var prevA = 0;

// // function render(a) {
// //   requestAnimationFrame(render);
// //   for (var i = 0; i < splines.length; i++) {
// //     for (var j = 0; j < splines[i].geometry.vertices.length; j++) {
// //       var vector = splines[i].geometry.vertices[j];
// //       vector.y =
// //         noise.simplex2(j * 0.05 + i - offset, a * splines[i].speed) * 8;
// //       vector.z = noise.simplex2(vector.x * 0.05 + i, a * splines[i].speed) * 8;

// //       vector.y *= 1 - Math.abs(vector.x / length);
// //       vector.z *= 1 - Math.abs(vector.x / length);
// //     }
// //     splines[i].geometry.verticesNeedUpdate = true;
// //   }
// //   scene.rotation.x = a * 0.0003;
// //   if (isMouseDown) {
// //     mouseJump.x += 0.001;
// //     if (a - prevA > 100) {
// //       updateColor();
// //       prevA = a;
// //     }
// //   } else {
// //     mouseJump.x -= 0.001;
// //   }
// //   mouseJump.x = Math.max(0, Math.min(0.07, mouseJump.x));
// //   offset += mouseJump.x;
// //   renderer.render(scene, camera);
// // }
// // var splines = [];
// // for (var i = 0; i < 12; i++) splines.push(new Spline());

// // function onResize() {
// //   camera.aspect = window.innerWidth / window.innerHeight;
// //   camera.updateProjectionMatrix();
// //   renderer.setSize(window.innerWidth, window.innerHeight);
// // }

// // function updateColor() {
// //   for (var i = 0; i < splines.length; i++) {
// //     var color = Math.abs((splines[i].color - offset * 10) % 360);
// //     for (var j = 0; j < splines[i].geometry.vertices.length; j++) {
// //       splines[i].mesh.geometry.colors[j] = new THREE.Color(
// //         "hsl(" + (j * 0.6 + color) + ",70%,70%)"
// //       );
// //     }
// //     splines[i].mesh.geometry.colorsNeedUpdate = true;
// //   }
// // }

// // function onMouseDown(e) {
// //   isMouseDown = true;
// //   return false;
// // }

// // function onMouseUp() {
// //   isMouseDown = false;
// // }
// // window.addEventListener("resize", onResize);
// // window.addEventListener("keydown", onMouseDown);
// // document.body.addEventListener("mousedown", onMouseDown);
// // document.body.addEventListener("mouseup", onMouseUp);
// // document.body.addEventListener("touchstart", onMouseDown);
// // document.body.addEventListener("touchend", onMouseUp);
// // requestAnimationFrame(render);
// /* ---- particles.js config ---- */

// particlesJS("particles-js", {
//   "particles": {
//     "number": {
//       "value": 380,
//       "density": {
//         "enable": true,
//         "value_area": 800
//       }
//     },
//     "color": {
//       "value": "#ffffff"
//     },
//     "shape": {
//       "type": "circle",
//       "stroke": {
//         "width": 0,
//         "color": "#000000"
//       },
//       "polygon": {
//         "nb_sides": 5
//       },
//       "image": {
//         "src": "img/github.svg",
//         "width": 100,
//         "height": 100
//       }
//     },
//     "opacity": {
//       "value": 0.5,
//       "random": false,
//       "anim": {
//         "enable": false,
//         "speed": 1,
//         "opacity_min": 0.1,
//         "sync": false
//       }
//     },
//     "size": {
//       "value": 3,
//       "random": true,
//       "anim": {
//         "enable": false,
//         "speed": 40,
//         "size_min": 0.1,
//         "sync": false
//       }
//     },
//     "line_linked": {
//       "enable": true,
//       "distance": 150,
//       "color": "#ffffff",
//       "opacity": 0.4,
//       "width": 1
//     },
//     "move": {
//       "enable": true,
//       "speed": 6,
//       "direction": "none",
//       "random": false,
//       "straight": false,
//       "out_mode": "out",
//       "bounce": false,
//       "attract": {
//         "enable": false,
//         "rotateX": 600,
//         "rotateY": 1200
//       }
//     }
//   },
//   "interactivity": {
//     "detect_on": "canvas",
//     "events": {
//       "onhover": {
//         "enable": true,
//         "mode": "grab"
//       },
//       "onclick": {
//         "enable": true,
//         "mode": "push"
//       },
//       "resize": true
//     },
//     "modes": {
//       "grab": {
//         "distance": 140,
//         "line_linked": {
//           "opacity": 1
//         }
//       },
//       "bubble": {
//         "distance": 400,
//         "size": 40,
//         "duration": 2,
//         "opacity": 8,
//         "speed": 3
//       },
//       "repulse": {
//         "distance": 200,
//         "duration": 0.4
//       },
//       "push": {
//         "particles_nb": 4
//       },
//       "remove": {
//         "particles_nb": 2
//       }
//     }
//   },
//   "retina_detect": true
// });


// /* ---- stats.js config ---- */

// var count_particles, stats, update;
// stats = new Stats;
// stats.setMode(0);
// stats.domElement.style.position = 'absolute';
// stats.domElement.style.left = '0px';
// stats.domElement.style.top = '0px';
// document.body.appendChild(stats.domElement);
// count_particles = document.querySelector('.js-count-particles');
// update = function () {
//   stats.begin();
//   stats.end();
//   if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {
//     count_particles.innerText = window.pJSDom[0].pJS.particles.array.length;
//   }
//   requestAnimationFrame(update);
// };
// requestAnimationFrame(update);

particlesJS("particles-js", {
  "particles": {
    "number": {
      "value": 380,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": {
      "value": "#ffffff"
    },
    "shape": {
      "type": "circle",
      "stroke": {
        "width": 0,
        "color": "#000000"
      },
      "polygon": {
        "nb_sides": 5
      },
      "image": {
        "src": "img/github.svg",
        "width": 100,
        "height": 100
      }
    },
    "opacity": {
      "value": 0.5,
      "random": false,
      "anim": {
        "enable": false,
        "speed": 1,
        "opacity_min": 0.1,
        "sync": false
      }
    },
    "size": {
      "value": 3,
      "random": true,
      "anim": {
        "enable": false,
        "speed": 40,
        "size_min": 0.1,
        "sync": false
      }
    },
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#ffffff",
      "opacity": 0.4,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 6,
      "direction": "none",
      "random": false,
      "straight": false,
      "out_mode": "out",
      "bounce": false,
      "attract": {
        "enable": false,
        "rotateX": 600,
        "rotateY": 1200
      }
    }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": {
        "enable": true,
        "mode": "grab"
      },
      "onclick": {
        "enable": true,
        "mode": "push"
      },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 140,
        "line_linked": {
          "opacity": 1
        }
      },
      "bubble": {
        "distance": 400,
        "size": 40,
        "duration": 2,
        "opacity": 8,
        "speed": 3
      },
      "repulse": {
        "distance": 200,
        "duration": 0.4
      },
      "push": {
        "particles_nb": 4
      },
      "remove": {
        "particles_nb": 2
      }
    }
  },
  "retina_detect": true
});


/* ---- stats.js config ---- */

var count_particles, stats, update;
stats = new Stats;
stats.setMode(0);
stats.domElement.style.position = 'absolute';
stats.domElement.style.left = '0px';
stats.domElement.style.top = '0px';
document.body.appendChild(stats.domElement);
count_particles = document.querySelector('.js-count-particles');
update = function () {
  stats.begin();
  stats.end();
  if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {
    count_particles.innerText = window.pJSDom[0].pJS.particles.array.length;
  }
  requestAnimationFrame(update);
};
requestAnimationFrame(update);