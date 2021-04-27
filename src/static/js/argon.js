
/*!

=========================================================
* Argon Dashboard - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard/blob/master/LICENSE.md)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/



//
// Layout
//

'use strict';

var Layout = (function() {

    function pinSidenav() {
        $('.sidenav-toggler').addClass('active');
        $('.sidenav-toggler').data('action', 'sidenav-unpin');
        $('body').removeClass('g-sidenav-hidden').addClass('g-sidenav-show g-sidenav-pinned');
        $('body').append('<div class="backdrop d-xl-none" data-action="sidenav-unpin" data-target='+$('#sidenav-main').data('target')+' />');

        // Store the sidenav state in a cookie session
        Cookies.set('sidenav-state', 'pinned');
    }

    function unpinSidenav() {
        $('.sidenav-toggler').removeClass('active');
        $('.sidenav-toggler').data('action', 'sidenav-pin');
        $('body').removeClass('g-sidenav-pinned').addClass('g-sidenav-hidden');
        $('body').find('.backdrop').remove();

        // Store the sidenav state in a cookie session
        Cookies.set('sidenav-state', 'unpinned');
    }

	document.querySelector('#close').addEventListener('click', function(){
		unpinSidenav()
		$('body').removeClass('nav-open')
	})

    // Set sidenav state from cookie

    var $sidenavState = Cookies.get('sidenav-state') ? Cookies.get('sidenav-state') : 'pinned';

    if($(window).width() > 1200) {
        if($sidenavState == 'pinned') {
            pinSidenav()
        }

        if(Cookies.get('sidenav-state') == 'unpinned') {
            unpinSidenav()
        }

        $(window).resize(function() {
            if( $('body').hasClass('g-sidenav-show') && !$('body').hasClass('g-sidenav-pinned')) {
                $('body').removeClass('g-sidenav-show').addClass('g-sidenav-hidden');
            }
        })
    }

    if($(window).width() < 1200){
      $('body').removeClass('g-sidenav-hide').addClass('g-sidenav-hidden');
      $('body').removeClass('g-sidenav-show');
      $(window).resize(function() {
          if( $('body').hasClass('g-sidenav-show') && !$('body').hasClass('g-sidenav-pinned')) {
              $('body').removeClass('g-sidenav-show').addClass('g-sidenav-hidden');
          }
      })
    }



    $("body").on("click", "[data-action]", function(e) {

        e.preventDefault();

        var $this = $(this);
        var action = $this.data('action');
        var target = $this.data('target');


        // Manage actions

        switch (action) {
            case 'sidenav-pin':
                pinSidenav();
            break;

            case 'sidenav-unpin':
                unpinSidenav();
            break;

            case 'search-show':
                target = $this.data('target');
                $('body').removeClass('g-navbar-search-show').addClass('g-navbar-search-showing');

                setTimeout(function() {
                    $('body').removeClass('g-navbar-search-showing').addClass('g-navbar-search-show');
                }, 150);

                setTimeout(function() {
                    $('body').addClass('g-navbar-search-shown');
                }, 300)
            break;

            case 'search-close':
                target = $this.data('target');
                $('body').removeClass('g-navbar-search-shown');

                setTimeout(function() {
                    $('body').removeClass('g-navbar-search-show').addClass('g-navbar-search-hiding');
                }, 150);

                setTimeout(function() {
                    $('body').removeClass('g-navbar-search-hiding').addClass('g-navbar-search-hidden');
                }, 300);

                setTimeout(function() {
                    $('body').removeClass('g-navbar-search-hidden');
                }, 500);
            break;
        }
    })


    // Add sidenav modifier classes on mouse events

    $('.sidenav').on('mouseenter', function() {
        if(! $('body').hasClass('g-sidenav-pinned')) {
            $('body').removeClass('g-sidenav-hide').removeClass('g-sidenav-hidden').addClass('g-sidenav-show');
        }
    })

    $('.sidenav').on('mouseleave', function() {
        if(! $('body').hasClass('g-sidenav-pinned')) {
            $('body').removeClass('g-sidenav-show').addClass('g-sidenav-hide');

            setTimeout(function() {
                $('body').removeClass('g-sidenav-hide').addClass('g-sidenav-hidden');
            }, 300);
        }
    })


    // Make the body full screen size if it has not enough content inside
    $(window).on('load resize', function() {
        if($('body').height() < 800) {
            $('body').css('min-height', '100vh');
            $('#footer-main').addClass('footer-auto-bottom')
        }
    })

})();

//
// Charts
//

'use strict';

var Charts = (function() {

	// Variable

	var $toggle = $('[data-toggle="chart"]');
	var mode = 'light';//(themeMode) ? themeMode : 'light';
	var fonts = {
		base: 'Open Sans'
	}

	// Colors
	var colors = {
		gray: {
			100: '#f6f9fc',
			200: '#e9ecef',
			300: '#dee2e6',
			400: '#ced4da',
			500: '#adb5bd',
			600: '#8898aa',
			700: '#525f7f',
			800: '#32325d',
			900: '#212529'
		},
		theme: {
			'default': '#172b4d',
			'primary': '#5e72e4',
			'secondary': '#f4f5f7',
			'info': '#11cdef',
			'success': '#2dce89',
			'danger': '#f5365c',
			'warning': '#fb6340'
		},
		black: '#12263F',
		white: '#FFFFFF',
		transparent: 'transparent',
	};


	// Methods

	// Chart.js global options
	function chartOptions() {

		// Options
		var options = {
			defaults: {
				global: {
					responsive: true,
					maintainAspectRatio: false,
					defaultColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
					defaultFontColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
					defaultFontFamily: fonts.base,
					defaultFontSize: 13,
					layout: {
						padding: 0
					},
					legend: {
						display: false,
						position: 'bottom',
						labels: {
							usePointStyle: true,
							padding: 16
						}
					},
					elements: {
						point: {
							radius: 0,
							backgroundColor: colors.theme['primary']
						},
						line: {
							tension: .4,
							borderWidth: 4,
							borderColor: colors.theme['primary'],
							backgroundColor: colors.transparent,
							borderCapStyle: 'rounded'
						},
						rectangle: {
							backgroundColor: colors.theme['warning']
						},
						arc: {
							backgroundColor: colors.theme['primary'],
							borderColor: (mode == 'dark') ? colors.gray[800] : colors.white,
							borderWidth: 4
						}
					},
					tooltips: {
						enabled: true,
						mode: 'index',
						intersect: false,
					}
				},
				doughnut: {
					cutoutPercentage: 83,
					legendCallback: function(chart) {
						var data = chart.data;
						var content = '';

						data.labels.forEach(function(label, index) {
							var bgColor = data.datasets[0].backgroundColor[index];

							content += '<span class="chart-legend-item">';
							content += '<i class="chart-legend-indicator" style="background-color: ' + bgColor + '"></i>';
							content += label;
							content += '</span>';
						});

						return content;
					}
				}
			}
		}

		// yAxes
		Chart.scaleService.updateScaleDefaults('linear', {
			gridLines: {
				borderDash: [2],
				borderDashOffset: [2],
				color: (mode == 'dark') ? colors.gray[900] : colors.gray[300],
				drawBorder: false,
				drawTicks: false,
				drawOnChartArea: true,
				zeroLineWidth: 0,
				zeroLineColor: 'rgba(0,0,0,0)',
				zeroLineBorderDash: [2],
				zeroLineBorderDashOffset: [2]
			},
			ticks: {
				beginAtZero: true,
				// suggestedMax: 8000,
				padding: 10,
				callback: function(value) {
					if (!(value % 10)) {
						return value
					}
				}
			}
		});

		// xAxes
		Chart.scaleService.updateScaleDefaults('category', {
			gridLines: {
				drawBorder: false,
				drawOnChartArea: false,
				drawTicks: false
			},
			ticks: {
				padding: 20
			},
			maxBarThickness: 10
		});

		return options;

	}

	// Parse global options
	function parseOptions(parent, options) {
		for (var item in options) {
			if (typeof options[item] !== 'object') {
				parent[item] = options[item];
			} else {
				parseOptions(parent[item], options[item]);
			}
		}
	}

	// Push options
	function pushOptions(parent, options) {
		for (var item in options) {
			if (Array.isArray(options[item])) {
				options[item].forEach(function(data) {
					parent[item].push(data);
				});
			} else {
				pushOptions(parent[item], options[item]);
			}
		}
	}

	// Pop options
	function popOptions(parent, options) {
		for (var item in options) {
			if (Array.isArray(options[item])) {
				options[item].forEach(function(data) {
					parent[item].pop();
				});
			} else {
				popOptions(parent[item], options[item]);
			}
		}
	}

	// Toggle options
	function toggleOptions(elem) {
		var options = elem.data('add');
		var $target = $(elem.data('target'));
		var $chart = $target.data('chart');

		if (elem.is(':checked')) {

			// Add options
			pushOptions($chart, options);

			// Update chart
			$chart.update();
		} else {

			// Remove options
			popOptions($chart, options);

			// Update chart
			$chart.update();
		}
	}

	// Update options
	function updateOptions(elem) {
		var options = elem.data('update');
		var $target = $(elem.data('target'));
		var $chart = $target.data('chart');

		// Parse options
		parseOptions($chart, options);

		// Toggle ticks
		toggleTicks(elem, $chart);

		// Update chart
		$chart.update();
	}

	// Toggle ticks
	function toggleTicks(elem, $chart) {

		if (elem.data('prefix') !== undefined || elem.data('prefix') !== undefined) {
			var prefix = elem.data('prefix') ? elem.data('prefix') : '';
			var suffix = elem.data('suffix') ? elem.data('suffix') : '';

			// Update ticks
			$chart.options.scales.yAxes[0].ticks.callback = function(value) {
				if (!(value % 10)) {
					return prefix + value + suffix;
				}
			}

			// Update tooltips
			$chart.options.tooltips.callbacks.label = function(item, data) {
				var label = data.datasets[item.datasetIndex].label || '';
				var yLabel = item.yLabel;
				var content = '';

				if (data.datasets.length > 1) {
					content += '<span class="popover-body-label mr-auto">' + label + '</span>';
				}

				content += '<span class="popover-body-value">' + prefix + yLabel + suffix + '</span>';
				return content;
			}

		}
	}


	// Events

	// Parse global options
	if (window.Chart) {
		parseOptions(Chart, chartOptions());
	}

	// Toggle options
	$toggle.on({
		'change': function() {
			var $this = $(this);

			if ($this.is('[data-add]')) {
				toggleOptions($this);
			}
		},
		'click': function() {
			var $this = $(this);

			if ($this.is('[data-update]')) {
				updateOptions($this);
			}
		}
	});


	// Return

	return {
		colors: colors,
		fonts: fonts,
		mode: mode
	};

})();

//
// Icon code copy/paste
//

'use strict';

var CopyIcon = (function() {

	// Variables

	var $element = '.btn-icon-clipboard',
		$btn = $($element);


	// Methods

	function init($this) {
		$this.tooltip().on('mouseleave', function() {
			// Explicitly hide tooltip, since after clicking it remains
			// focused (as it's a button), so tooltip would otherwise
			// remain visible until focus is moved away
			$this.tooltip('hide');
		});

		var clipboard = new ClipboardJS($element);

		clipboard.on('success', function(e) {
			$(e.trigger)
				.attr('title', 'Copied!')
				.tooltip('_fixTitle')
				.tooltip('show')
				.attr('title', 'Copy to clipboard')
				.tooltip('_fixTitle')

			e.clearSelection()
		});
	}


	// Events
	if ($btn.length) {
		init($btn);
	}

})();

//
// Navbar
//

'use strict';

var Navbar = (function() {

	// Variables

	var $nav = $('.navbar-nav, .navbar-nav .nav');
	var $collapse = $('.navbar .collapse');
	var $dropdown = $('.navbar .dropdown');

	// Methods

	function accordion($this) {
		$this.closest($nav).find($collapse).not($this).collapse('hide');
	}

    function closeDropdown($this) {
        var $dropdownMenu = $this.find('.dropdown-menu');

        $dropdownMenu.addClass('close');

    	setTimeout(function() {
    		$dropdownMenu.removeClass('close');
    	}, 200);
	}


	// Events

	$collapse.on({
		'show.bs.collapse': function() {
			accordion($(this));
		}
	})

	$dropdown.on({
		'hide.bs.dropdown': function() {
			closeDropdown($(this));
		}
	})

})();


//
// Navbar collapse
//


var NavbarCollapse = (function() {

	// Variables

	var $nav = $('.navbar-nav'),
		$collapse = $('.navbar .navbar-custom-collapse');


	// Methods

	function hideNavbarCollapse($this) {
		$this.addClass('collapsing-out');
	}

	function hiddenNavbarCollapse($this) {
		$this.removeClass('collapsing-out');
	}


	// Events

	if ($collapse.length) {
		$collapse.on({
			'hide.bs.collapse': function() {
				hideNavbarCollapse($collapse);
			}
		})

		$collapse.on({
			'hidden.bs.collapse': function() {
				hiddenNavbarCollapse($collapse);
			}
		})
	}

	var navbar_menu_visible = 0;

	$( ".sidenav-toggler" ).click(function() {
		if(navbar_menu_visible == 1){
		  $('body').removeClass('nav-open');
			navbar_menu_visible = 0;
			$('.bodyClick').remove();

		} else {

		var div = '<div class="bodyClick"></div>';
		$(div).appendTo('body').click(function() {
				 $('body').removeClass('nav-open');
					navbar_menu_visible = 0;
					$('.bodyClick').remove();
					
			 });

		 $('body').addClass('nav-open');
			navbar_menu_visible = 1;

		}

	});

})();

//
// Popover
//

'use strict';

var Popover = (function() {

	// Variables

	var $popover = $('[data-toggle="popover"]'),
		$popoverClass = '';


	// Methods

	function init($this) {
		if ($this.data('color')) {
			$popoverClass = 'popover-' + $this.data('color');
		}

		var options = {
			trigger: 'focus',
			template: '<div class="popover ' + $popoverClass + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
		};

		$this.popover(options);
	}


	// Events

	if ($popover.length) {
		$popover.each(function() {
			init($(this));
		});
	}

})();

//
// Scroll to (anchor links)
//

'use strict';

var ScrollTo = (function() {

	//
	// Variables
	//

	var $scrollTo = $('.scroll-me, [data-scroll-to], .toc-entry a');


	//
	// Methods
	//

	function scrollTo($this) {
		var $el = $this.attr('href');
        var offset = $this.data('scroll-to-offset') ? $this.data('scroll-to-offset') : 0;
		var options = {
			scrollTop: $($el).offset().top - offset
		};

        // Animate scroll to the selected section
        $('html, body').stop(true, true).animate(options, 600);

        event.preventDefault();
	}


	//
	// Events
	//

	if ($scrollTo.length) {
		$scrollTo.on('click', function(event) {
			scrollTo($(this));
		});
	}

})();

//
// Tooltip
//

'use strict';

var Tooltip = (function() {

	// Variables

	var $tooltip = $('[data-toggle="tooltip"]');


	// Methods

	function init() {
		$tooltip.tooltip();
	}


	// Events

	if ($tooltip.length) {
		init();
	}

})();

//
// Form control
//

'use strict';

var FormControl = (function() {

	// Variables

	var $input = $('.form-control');


	// Methods

	function init($this) {
		$this.on('focus blur', function(e) {
        $(this).parents('.form-group').toggleClass('focused', (e.type === 'focus'));
    }).trigger('blur');
	}


	// Events

	if ($input.length) {
		init($input);
	}

})();

//
// Google maps
//

var $map = $('#map-default'),
    map,
    lat,
    lng,
    color = "#5e72e4";

function initMap() {

    map = document.getElementById('map-default');
    lat = map.getAttribute('data-lat');
    lng = map.getAttribute('data-lng');

    var myLatlng = new google.maps.LatLng(lat, lng);
    var mapOptions = {
        zoom: 12,
        scrollwheel: false,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
    }

    map = new google.maps.Map(map, mapOptions);

    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        animation: google.maps.Animation.DROP,
        title: 'Hello World!'
    });

    var contentString = '<div class="info-window-content"><h2>Argon Dashboard</h2>' +
        '<p>A beautiful Dashboard for Bootstrap 4. It is Free and Open Source.</p></div>';

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
    });
}

if($map.length) {
    google.maps.event.addDomListener(window, 'load', initMap);
}

//
// Bars chart
//

var BarsChart = (function() {

	//
	// Variables
	//

	var $chart = $('#chart-doughnut');


	//
	// Methods
	//

	// Init chart
	function initChart($chart) {
		var seriesData = [parseInt(document.querySelector('#bugs').innerText), parseInt(document.querySelector('#vulnerabilities').innerText), parseInt(document.querySelector('#codeSmells').innerText)]
		var total = seriesData.reduce((a, v) => a + v);
		var inPercent = seriesData.map(v => Math.max(v / total * 100, 1));
		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'pie',
			showTooltips: true,
			options: {
			legend: {
				display: true
				},
			tooltips: {
				callbacks: {
				  label: function(tooltipItem, data) {
					var value = inPercent[tooltipItem.index];
					var label = data.labels[tooltipItem.index];
					return `${label}: ${Math.round(value)}%`;
				  }
				}
			}
			},
			data: {
				labels: ['Bugs', 'Vulnerabilities', 'Code Smells'],
				datasets: [{
					backgroundColor: ["#0074D9", "#FF4136", "#2ECC40"],
					data: inPercent
				}]
			}
		});

		// Save to jQuery object
		$chart.data('chart', ordersChart);
	}


	// Init chart
	if ($chart.length) {
		initChart($chart);
	}

})();

'use strict';

//
// Sales chart
//

const horizontalChartData = eval(document.getElementById('horizontalChartData').innerText)

var SalesChart = (function() {

  // Variables

  var $chart = $('#chart-sales-dark');


  // Methods

  function init($chart) {

    var salesChart = new Chart($chart, {
      type: 'horizontalBar',
      options: {
        scales: {
          yAxes: [{
            gridLines: {
              lineWidth: 1,
              color: Charts.colors.gray[900],
              zeroLineColor: Charts.colors.gray[900]
            },
			legend: {
				display: true
				},
            ticks: {
              callback: function(value) {
                if (!(value % 10)) {
                  return value;
                }
              }
            }
          }]
        },
        tooltips: {
          callbacks: {
            label: function(item, data) {
              var label = data.datasets[item.datasetIndex].label || '';
              var yLabel = item.xLabel;
              var content = '';

              if (data.datasets.length > 1) {
                content += '<span class="popover-body-label mr-auto">' + label + '</span>';
              }

              content += yLabel;
              return content;
            }
          }
        }
      },
      data: {
        labels:  horizontalChartData[0],
        datasets: [{
          label: 'Performance',
          data:  horizontalChartData[1]
        }]
      },
    });

    // Save to jQuery object

    $chart.data('chart', salesChart);

  };


  // Events

  if ($chart.length) {
    init($chart);
  }

})();

//
// Bootstrap Datepicker
//

'use strict';

var Datepicker = (function() {

	// Variables

	var $datepicker = $('.datepicker');


	// Methods

	function init($this) {
		var options = {
			disableTouchKeyboard: true,
			autoclose: false
		};

		$this.datepicker(options);
	}


	// Events

	if ($datepicker.length) {
		$datepicker.each(function() {
			init($(this));
		});
	}

})();

//
// Form control
//

'use strict';

var noUiSlider = (function() {

	// Variables

	// var $sliderContainer = $('.input-slider-container'),
	// 		$slider = $('.input-slider'),
	// 		$sliderId = $slider.attr('id'),
	// 		$sliderMinValue = $slider.data('range-value-min');
	// 		$sliderMaxValue = $slider.data('range-value-max');;


	// // Methods
	//
	// function init($this) {
	// 	$this.on('focus blur', function(e) {
  //       $this.parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
  //   }).trigger('blur');
	// }
	//
	//
	// // Events
	//
	// if ($input.length) {
	// 	init($input);
	// }



	if ($(".input-slider-container")[0]) {
			$('.input-slider-container').each(function() {

					var slider = $(this).find('.input-slider');
					var sliderId = slider.attr('id');
					var minValue = slider.data('range-value-min');
					var maxValue = slider.data('range-value-max');

					var sliderValue = $(this).find('.range-slider-value');
					var sliderValueId = sliderValue.attr('id');
					var startValue = sliderValue.data('range-value-low');

					var c = document.getElementById(sliderId),
							d = document.getElementById(sliderValueId);

					noUiSlider.create(c, {
							start: [parseInt(startValue)],
							connect: [true, false],
							//step: 1000,
							range: {
									'min': [parseInt(minValue)],
									'max': [parseInt(maxValue)]
							}
					});

					c.noUiSlider.on('update', function(a, b) {
							d.textContent = a[b];
					});
			})
	}

	if ($("#input-slider-range")[0]) {
			var c = document.getElementById("input-slider-range"),
					d = document.getElementById("input-slider-range-value-low"),
					e = document.getElementById("input-slider-range-value-high"),
					f = [d, e];

			noUiSlider.create(c, {
					start: [parseInt(d.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
					connect: !0,
					range: {
							min: parseInt(c.getAttribute('data-range-value-min')),
							max: parseInt(c.getAttribute('data-range-value-max'))
					}
			}), c.noUiSlider.on("update", function(a, b) {
					f[b].textContent = a[b]
			})
	}

})();

//
// Scrollbar
//

'use strict';

var Scrollbar = (function() {

	// Variables

	var $scrollbar = $('.scrollbar-inner');


	// Methods

	function init() {
		$scrollbar.scrollbar().scrollLock()
	}


	// Events

	if ($scrollbar.length) {
		init();
	}

})();


const bubbleData = eval(document.getElementById('bubble').innerText)
Array.from(bubbleData).forEach(element => {
	let str = "";
	let hours = Math.floor(element["reliabilityEffort"]/60)
	if(hours > 8){
		let days = Math.floor(hours/8)
		let corhours = hours
		while (corhours > 8){
			corhours -= 8
		}
		str += `${days}d${corhours}h`
	}
	else{
		let mins = Math.floor(element["reliabilityEffort"]%60)
		str += `${hours}h${mins}m` 
	}
})

function r() { return Math.floor(Math.random() * 255) }

let Reliabilityarr = [];
Array.from(bubbleData).forEach(element => {
	let rating = element["reliabilityRating"]
	console.log(rating)
	let color;
	// if(rating == "1.0"){
	// 	color = 'rgb(204,238,204)'
	// }
	// else if(rating == "2.0"){
	// 	color = 'rgb(239,247,208)'
	// }
	// else if(rating == "3.0"){
	// 	color = 'rgb(251,242,205)'
	// }
	// else if(rating == "4.0"){
	// 	color = 'rgb(251,229,210)'
	// }
	// else if(rating == "5.0"){
	// 	color =  'rgb(246,214,217)'
	// }
	let rate;
	if(rating == "1.0"){
		color = 'rgb(14,175,14)'
		rate = 'A'
	}
	else if(rating == "2.0"){
		color = 'rgb(180,215,32)'
		rate = 'B'
	}
	else if(rating == "3.0"){
		color = 'rgb(240,210,81)'
		rate = 'C'
	}
	else if(rating == "4.0"){
		color = 'rgb(239,140,58)'
		rate = 'D'
	}
	else if(rating == "5.0"){
		color =  'rgb(212,52,64)'
		rate = 'E'
	}
	let str = "";
	let hours = Math.floor(element["reliabilityEffort"]/60)
	if(hours > 8){
		let days = Math.floor(hours/8)
		let corhours = hours
		while (corhours > 8){
			corhours -= 8
		}
		str += `${days}d${corhours}h`
	}
	else{
		let mins = Math.floor(element["reliabilityEffort"]%60)
		str += `${hours}h${mins}m` 
	}
	Reliabilityarr.push({"title":element["projectName"],"color": color, "x":parseInt(element["linesOfCodes"]), "y":parseInt(element["bugs"]), "time": str, "value":parseInt(element["reliabilityEffort"]), "rating":rate})
})

let Securityarr = []
Array.from(bubbleData).forEach(element => {
	let rating = element["securityRating"]
	let color;
	let rate;
	if(rating == "1.0"){
		color = 'rgb(14,175,14)'
		rate = 'A'
	}
	else if(rating == "2.0"){
		color = 'rgb(180,215,32)'
		rate = 'B'
	}
	else if(rating == "3.0"){
		color = 'rgb(240,210,81)'
		rate = 'C'
	}
	else if(rating == "4.0"){
		color = 'rgb(239,140,58)'
		rate = 'D'
	}
	else if(rating == "5.0"){
		color =  'rgb(212,52,64)'
		rate = 'E'
	}
	let str = "";
	let hours = Math.floor(element["securityEffort"]/60)
	if(hours > 8){
		let days = Math.floor(hours/8)
		let corhours = hours
		while (corhours > 8){
			corhours -= 8
		}
		str += `${days}d${corhours}h`
	}
	else{
		let mins = Math.floor(element["securityEffort"]%60)
		str += `${hours}h${mins}m` 
	}
	Securityarr.push({"title":element["projectName"],"color": color, "x":parseInt(element["linesOfCodes"]), "y":parseInt(element["vulnerabilities"]), "time": str, "value":parseInt(element["securityEffort"]), "rating":rate})
})

let Maintainabilityarr = []
Array.from(bubbleData).forEach(element => {
	let rating = element["maintainabilityRating"]
	let color;
	let rate;
	if(rating == "1.0"){
		color = 'rgb(14,175,14)'
		rate = 'A'
	}
	else if(rating == "2.0"){
		color = 'rgb(180,215,32)'
		rate = 'B'
	}
	else if(rating == "3.0"){
		color = 'rgb(240,210,81)'
		rate = 'C'
	}
	else if(rating == "4.0"){
		color = 'rgb(239,140,58)'
		rate = 'D'
	}
	else if(rating == "5.0"){
		color =  'rgb(212,52,64)'
		rate = 'E'
	}
	let str = "";
	let hours = Math.floor(element["maintainabilityEffort"]/60)
	if(hours > 8){
		let days = Math.floor(hours/8)
		let corhours = hours
		while (corhours > 8){
			corhours -= 8
		}
		str += `${days}d${corhours}h`
	}
	else{
		let mins = Math.floor(element["maintainabilityEffort"]%60)
		str += `${hours}h${mins}m` 
	}
	Maintainabilityarr.push({"title":element["projectName"],"color": color, "x":parseInt(element["linesOfCodes"]), "y":parseInt(element["code_smells"]), "time": str, "value":parseInt(element["maintainabilityEffort"]), "rating":rate})
})

let Dupearr = []
Array.from(bubbleData).forEach(element => {
	function r() { return Math.floor(Math.random() * 255) }
	let color = 'rgb(' + r() + "," + r() + "," + r() + ')';
	Dupearr.push({"title":element["projectName"],
	"color": color, "x":parseInt(element["linesOfCodes"]), 
	"y":parseFloat(element["duplicatePercentage"]), 
	"blocks":parseInt(element["duplicateBlocks"]), 
	"value":parseFloat(element["duplicateBlocks"])})
})
// arr.sort((a,b) => a["y"] - b["y"])
// var index = 0
// arr.forEach(element => {
// 	element['value'] = index
// 	index += 1 
// })

// arr.push({
//     "y": 0,
//     "x": 0,
//     "value": 1,
//   })
// arr.push({
//     "y": 0,
//     "x": 0,
//     "value": arr[arr.length-1][""],
//   })

function renderChart(arr){

	arr.sort((a,b) => a["y"] - b["y"])
	console.log(arr)
		
	am4core.useTheme(am4themes_animated);
	am4core.useTheme(am4themes_dark);

	var chart = am4core.create("chartdiv", am4charts.XYChart);
	chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

	var valueAxisX = chart.xAxes.push(new am4charts.ValueAxis());
	var valueAxisY = chart.yAxes.push(new am4charts.ValueAxis());

	let topContainer = chart.chartContainer.createChild(am4core.Container);
	topContainer.layout = "absolute";
	topContainer.toBack();
	topContainer.paddingBottom = 15;
	topContainer.width = am4core.percent(100);
	
	let axisTitle = topContainer.createChild(am4core.Label);
	axisTitle.text = "y - Number of Bugs";
	axisTitle.fontWeight = 600;
	axisTitle.align = "left";
	axisTitle.paddingLeft = 10;

	var label = chart.chartContainer.createChild(am4core.Label);
	label.text = "x - Lines of Codes";
	label.align = "center";
	label.paddingTop = 10;

	valueAxisY.min = 0;
	valueAxisY.max = arr[arr.length-1]["y"] + 100; 

	var series = chart.series.push(new am4charts.LineSeries());
	series.dataFields.valueX = "x";
	series.dataFields.valueY = "y";
	series.dataFields.value = "value";
	series.strokeOpacity = 0;
	series.sequencedInterpolation = true;
	series.legendSettings.labelText = "hi"

	var bullet = series.bullets.push(new am4core.Circle());
	bullet.fill = am4core.color("#ff0000");
	bullet.propertyFields.fill = "color";
	bullet.strokeOpacity = 0;
	bullet.radius = 5
	bullet.maxradius=10;
	bullet.strokeWidth = 2;
	bullet.fillOpacity = 0.7;
	bullet.stroke = am4core.color("#ffffff");

	bullet.tooltipText = "[bold]{title}:[/]\nTechnical Debt: {time}\nLines of Codes: {valueX.value}\nNumber of bugs:{valueY.value}\nReliability Rating: {rating}";

	var hoverState = bullet.states.create("hover");
	hoverState.properties.fillOpacity = 1;
	hoverState.properties.strokeOpacity = 1;

	series.heatRules.push({ target: bullet, min: 7, max: 30, property: "radius" });

	bullet.adapter.add("tooltipY", function (tooltipY, target) {
		return -target.radius;
	})

	chart.cursor = new am4charts.XYCursor();
	chart.cursor.behavior = "zoomXY";

	chart.scrollbarX = new am4core.Scrollbar();
	chart.scrollbarY = new am4core.Scrollbar();

	chart.data = arr
}

function renderChart2(arr){

	arr.sort((a,b) => a["y"] - b["y"])
		
	am4core.useTheme(am4themes_animated);
	am4core.useTheme(am4themes_dark);

	var chart = am4core.create("chartdiv", am4charts.XYChart);
	chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

	var valueAxisX = chart.xAxes.push(new am4charts.ValueAxis());
	var valueAxisY = chart.yAxes.push(new am4charts.ValueAxis());

	let topContainer = chart.chartContainer.createChild(am4core.Container);
	topContainer.layout = "absolute";
	topContainer.toBack();
	topContainer.paddingBottom = 15;
	topContainer.width = am4core.percent(100);
	
	let axisTitle = topContainer.createChild(am4core.Label);
	axisTitle.text = "y - Number of Vulnerabilities";
	axisTitle.fontWeight = 600;
	axisTitle.align = "left";
	axisTitle.paddingLeft = 10;

	var label = chart.chartContainer.createChild(am4core.Label);
	label.text = "x - Lines of Codes";
	label.align = "center";
	label.paddingTop = 10;

	valueAxisY.min = 0;
	valueAxisY.max = arr[arr.length-1]["y"] + 100; 

	var series = chart.series.push(new am4charts.LineSeries());
	series.dataFields.valueX = "x";
	series.dataFields.valueY = "y";
	series.dataFields.value = "value";
	series.strokeOpacity = 0;
	series.sequencedInterpolation = true;

	var bullet = series.bullets.push(new am4core.Circle());
	bullet.fill = am4core.color("#ff0000");
	bullet.propertyFields.fill = "color";
	bullet.strokeOpacity = 0;
	bullet.radius = 5
	bullet.maxradius=10;
	bullet.strokeWidth = 2;
	bullet.fillOpacity = 0.7;
	bullet.stroke = am4core.color("#ffffff");

	bullet.tooltipText = "[bold]{title}:[/]\nTechnical Debt: {time}\nLines of Codes: {valueX.value}\nNumber of Vulnerabilities:{valueY.value}\nSecurity Rating: {rating}";

	var hoverState = bullet.states.create("hover");
	hoverState.properties.fillOpacity = 1;
	hoverState.properties.strokeOpacity = 1;

	series.heatRules.push({ target: bullet, min: 7, max: 30, property: "radius" });

	bullet.adapter.add("tooltipY", function (tooltipY, target) {
		return -target.radius;
	})

	chart.cursor = new am4charts.XYCursor();
	chart.cursor.behavior = "zoomXY";

	chart.scrollbarX = new am4core.Scrollbar();
	chart.scrollbarY = new am4core.Scrollbar();

	chart.data = arr
}

function renderChart3(arr){

	arr.sort((a,b) => a["y"] - b["y"])

	am4core.useTheme(am4themes_animated);
	am4core.useTheme(am4themes_dark);

	var chart = am4core.create("chartdiv", am4charts.XYChart);
	chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

	var valueAxisX = chart.xAxes.push(new am4charts.ValueAxis());
	var valueAxisY = chart.yAxes.push(new am4charts.ValueAxis());

	let topContainer = chart.chartContainer.createChild(am4core.Container);
	topContainer.layout = "absolute";
	topContainer.toBack();
	topContainer.paddingBottom = 15;
	topContainer.width = am4core.percent(100);
	
	let axisTitle = topContainer.createChild(am4core.Label);
	axisTitle.text = "y - Number of Code Smells";
	axisTitle.fontWeight = 600;
	axisTitle.align = "left";
	axisTitle.paddingLeft = 10;

	var label = chart.chartContainer.createChild(am4core.Label);
	label.text = "x - Lines of Codes";
	label.align = "center";
	label.paddingTop = 10;

	valueAxisY.min = 0;
	valueAxisY.max = arr[arr.length-1]["y"] + 100; 

	var series = chart.series.push(new am4charts.LineSeries());
	series.dataFields.valueX = "x";
	series.dataFields.valueY = "y";
	series.dataFields.value = "value";
	series.strokeOpacity = 0;
	series.sequencedInterpolation = true;

	var bullet = series.bullets.push(new am4core.Circle());
	bullet.fill = am4core.color("#ff0000");
	bullet.propertyFields.fill = "color";
	bullet.strokeOpacity = 0;
	bullet.radius = 5
	bullet.maxradius=10;
	bullet.strokeWidth = 2;
	bullet.fillOpacity = 0.7;
	bullet.stroke = am4core.color("#ffffff");

	bullet.tooltipText = "[bold]{title}:[/]\nTechnical Debt: {time}\nLines of Codes: {valueX.value}\nNumber of Code Smells:{valueY.value}\nMaintability rating: {rating}";

	var hoverState = bullet.states.create("hover");
	hoverState.properties.fillOpacity = 1;
	hoverState.properties.strokeOpacity = 1;

	series.heatRules.push({ target: bullet, min: 7, max: 30, property: "radius" });

	bullet.adapter.add("tooltipY", function (tooltipY, target) {
		return -target.radius;
	})

	chart.cursor = new am4charts.XYCursor();
	chart.cursor.behavior = "zoomXY";

	chart.scrollbarX = new am4core.Scrollbar();
	chart.scrollbarY = new am4core.Scrollbar();

	chart.data = arr
}

function renderChart4(arr){

	arr.sort((a,b) => a["y"] - b["y"])

	am4core.useTheme(am4themes_animated);
	am4core.useTheme(am4themes_dark);

	var chart = am4core.create("chartdiv", am4charts.XYChart);
	chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

	var valueAxisX = chart.xAxes.push(new am4charts.ValueAxis());
	var valueAxisY = chart.yAxes.push(new am4charts.ValueAxis());

	let topContainer = chart.chartContainer.createChild(am4core.Container);
	topContainer.layout = "absolute";
	topContainer.toBack();
	topContainer.paddingBottom = 15;
	topContainer.width = am4core.percent(100);
	
	let axisTitle = topContainer.createChild(am4core.Label);
	axisTitle.text = "y - Duplicate Percentage";
	axisTitle.fontWeight = 600;
	axisTitle.align = "left";
	axisTitle.paddingLeft = 10;

	var label = chart.chartContainer.createChild(am4core.Label);
	label.text = "x - Lines of Codes";
	label.align = "center";
	label.paddingTop = 10;

	valueAxisY.min = 0;
	valueAxisY.max = arr[arr.length-1]["y"] + 10; 

	var series = chart.series.push(new am4charts.LineSeries());
	series.dataFields.valueX = "x";
	series.dataFields.valueY = "y";
	series.dataFields.value = "value";
	series.strokeOpacity = 0;
	series.sequencedInterpolation = true;

	var bullet = series.bullets.push(new am4core.Circle());
	bullet.fill = am4core.color("#ff0000");
	bullet.propertyFields.fill = "color";
	bullet.strokeOpacity = 0;
	bullet.radius = 5
	bullet.maxradius=10;
	bullet.strokeWidth = 2;
	bullet.fillOpacity = 0.7;
	bullet.stroke = am4core.color("#ffffff");

	bullet.tooltipText = "[bold]{title}:[/]\nLines of Codes: {valueX.value}\nDuplication Percentage:{valueY.value}\nDuplicated blocks:{blocks}";

	var hoverState = bullet.states.create("hover");
	hoverState.properties.fillOpacity = 1;
	hoverState.properties.strokeOpacity = 1;

	series.heatRules.push({ target: bullet, min: 7, max: 30, property: "radius" });

	bullet.adapter.add("tooltipY", function (tooltipY, target) {
		return -target.radius;
	})

	chart.cursor = new am4charts.XYCursor();
	chart.cursor.behavior = "zoomXY";

	chart.scrollbarX = new am4core.Scrollbar();
	chart.scrollbarY = new am4core.Scrollbar();

	chart.data = arr
}

renderChart(Reliabilityarr)

document.getElementById('click1').addEventListener('click', e=> {
	renderChart(Reliabilityarr)
	document.getElementById('title').innerText = 'Total number of bugs for each project'
	document.getElementById('colorTitle').innerText = 'Color: Reliability RatingSize: Bugs'
	Array.from(document.getElementsByClassName('legend-item')).forEach(element => {
		element.style.display = ''
	})
})
document.getElementById('click2').addEventListener('click', e=> {
	renderChart2(Securityarr)
	document.getElementById('title').innerText = 'Total number of vulnerabilities for each project'
	document.getElementById('colorTitle').innerText = 'Color: Security RatingSize: Vulnerabilities'
	Array.from(document.getElementsByClassName('legend-item')).forEach(element => {
		element.style.display = ''
	})
})
document.getElementById('click3').addEventListener('click', e=> {
	renderChart3(Maintainabilityarr)
	document.getElementById('title').innerText = 'Total number of code smells for each project'
	document.getElementById('colorTitle').innerText = 'Color: Maintainability RatingSize: Code Smells'
	Array.from(document.getElementsByClassName('legend-item')).forEach(element => {
		element.style.display = ''
	})
})
document.getElementById('click4').addEventListener('click', e=> {
	renderChart4(Dupearr)
	document.getElementById('title').innerText = 'Total number of duplicatied lines for each project'
	document.getElementById('colorTitle').innerText = "Size: Duplicated Blocks"
	Array.from(document.getElementsByClassName('legend-item')).forEach(element => {
		element.style.display = 'none'
	})
})



// let searchBar = document.querySelector('#search-item')
// searchBar.addEventListener('keyup', event =>{
//     Array.from(itemNames).forEach(name => {
//         let itemContent = name.parentElement.parentElement.parentElement
//         if (name.innerText.toLowerCase().indexOf(searchBar.value.toLowerCase()) == -1) {
//             itemContent.style.display = 'none';
//         }
//         else {
//             itemContent.style.display = 'block';
//         }
//     });
// });



