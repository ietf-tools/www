$(function(){

	/*
		Stick scroll sidebar
		 - initial version for prototype, needs calculation love to make it more re-usuable
	*/
	var stickyFix = function( ){

		var $stickyItem 							= $( '.sticky-item' ),
				$stickyContainer					= $( '.sticky-container' ),
				$pageWrapper 						= $( '.page-wrap' ),
				$bodyContainer						= $( 'body' ),
				$stickyFriends						= $( '.sticky-friend' ),
				$stickContents						= $( '.sticky-item .sticky-listing > li' ),
				listPadding							= '17',
				zIndex								= 11,
				breakpoint							= 1160,
				winWidth							= $(window).width(),
				fallbackClasses						= 'none float-right four', // these are classes that will be removed from the container, so that without JS the side-bar renders as-is

				// THESE two classes could/should be defined in CSS?
				stickyItemCSS 		= {
					'float'				: 'none',
					'position' 		: 'absolute',
					'overflow-x'	: 'hidden',
					'right'				: '0',
					'width'       : 'auto'
				},

				NONstickyItemCSS	= {
					'float' 			: 'none',
					'background'	: 'hotpink',
					'position' 		: 'relative',
					'overflow-x'	: 'hidden',
					'paddingLeft'	: listPadding + 'px',
					'right'				: '0',
					'z-index'			: zIndex
				};

		// if we have a sticky container
		if( $stickyItem[0] ){

			// If we are above the breakpoint defined
			if( winWidth > breakpoint ) {

				// remove classes and add initial styling
				$stickyItem.removeClass( fallbackClasses ).css( stickyItemCSS );

				// Calculated values that will depend on page structure
				var pageMargin						= ( ( $pageWrapper.width() - $pageWrapper.outerWidth() ) / 2 ), 	// auto generated margin used to center the page
						pagePadding						= ( ( $pageWrapper.innerWidth() - $pageWrapper.width() ) / 2 ),
						availableSpace				= ( $bodyContainer.width() - $stickyFriends.outerWidth() ),
						remainingGridSpace		= $stickyContainer.outerWidth() - $stickyFriends.outerWidth();

				// Values for sticky container and contents
				var	sideBarHeight					= $stickyFriends.innerHeight(),
						posRight							= (($(window).width() - $stickyContainer.outerWidth()) / 2), 			// This will depend on page structure
						sideBarWidth 					= $(window).width() - $stickyFriends.outerWidth() - posRight - 5, // 5px to add a bit of margin
						contentWidth  				= remainingGridSpace;

				// Apply our width and height
				$stickyItem.css({
					'width'		: sideBarWidth,
					'height' 	: sideBarHeight + 150,
					'right'		: -posRight
				});

				$stickContents.css({
					'width'	: contentWidth
				});

			// if we are below the breakpoint defined
			} else if ( winWidth <= breakpoint ){

				// remove classes and add initial styling
				$stickyItem.addClass( fallbackClasses ).removeAttr( 'style' );
				$stickContents.removeAttr( 'style' );
			}
		}
	}

	// Give the page a moment to render its CSS before using its layout to position the stickyItem
	setTimeout(function(){
		stickyFix();
	}, 50);
	// On browser resize run stickyFix
	$(window).on('resize', stickyFix);

	//tooltip
		$('.bibliography-item').each(function() {
				var ordering = $(this).find('.reference-ordering').text(),
						title = $(this).find('.reference-title').text(),
						longTitle = $(this).find('.reference-long-title').text(),
						link = $(this).find('.reference-link').attr('href'),
						content = $(this).children('.reference-cont').text();
				if (longTitle) {
						title = longTitle;
				}
				$(`<ul class="link-preview ordering-${ordering}"><li><h2>${title}</h2></li><li>${content}</li></ul>`).prependTo('.has-references');
				// Replace the bibliography reference with a link to the object itself
				$(`a[href="#bibliography${ordering}"]`).attr('href', ($(`a[name="bibliography${ordering}"]`).next().attr('href')));
		});

		$('.bibliography-reference').on('mouseenter mouseleave', function(){
				var $item = $(this),
						ordering = $item.data('ordering'),
						$tooltip = $(`.link-preview.ordering-${ordering}`),
						linkTop = $item.position().top; // get top position of hovered link
						$tooltip.toggleClass( 'show' ).css({top: linkTop});
		});

		$("#bibliography").hide();


//animating in this section toggle ===============================================================//

	$('.this-section').click(function () {
			$('.side-nav').toggle("slow");
	});

//mobile menu ====================================================================================//
	$('.more').click(function(){
			$('.more ul').toggleClass('show');
	});

	//geting height of nav-holder then animating from 0px to "height"
	$('.hamburger').click(function () {
			var el = $('.nav-holder'),
			curHeight = el.height(),
			autoHeight = el.css('height', 'auto').height();
			el.height(curHeight).animate({
					height: autoHeight == curHeight ? "0" : autoHeight
			}, 500);
	})

//read more ====================================================================================//
		$(function() {
				$('.more-wrapper').show();

				if ($('.read-more').length && $('.read-more-two').length) {
						$('.read-more').addClass('swap');
						$('.read-more-content-two').hide();
				}
				else if ($('.read-more').length) {
						$('.read-more').addClass('swap');
				}
				else if ($('.read-more-two').length) {
						$('.read-more-two').addClass('swap');
				}
		});

	$('.read-more').click(function () {
			$('.read-more-content').slideToggle();
			$('.read-more-two.swap').removeClass('swap');
			$('.read-more-content-two').slideUp();
	});

	$('.read-more-two').click(function () {
			$('.read-more-content-two').slideToggle();
			$('.read-more.swap').removeClass('swap');
			$('.read-more-content').slideUp();
	});

//Date picker ==================================================================================//

	$(function() {
		$( ".date-to" ).datepicker({
			dateFormat: "dd/mm/yy"
		});
	});

	$(function() {
		$( ".date-from" ).datepicker({
		dateFormat: "dd/mm/yy"
	});
	});

//read more // swap ============================================================================//
	$('.read-more').click(function(){
			$(this).toggleClass('swap');
	});

	$('.read-more-two').click(function(){
			$(this).toggleClass('swap');
	});

	$('.link-toggle').click(function(){
			$(this).next().toggleClass('show');
	});

	$('.link-toggle').click(function(){
			$(this).toggleClass('swap');
	});

	$('.this-section').click(function(){
			$(this).toggleClass('swap');
	});

	$('.link-toggle').click(function () {
			var el = $(this).next(),
			curHeight = el.height(),
			autoHeight = el.css('height', 'auto').height();
			el.height(curHeight).animate({
					height: autoHeight == curHeight ? "0" : autoHeight
			}, 500);
	})

//Showing search box ======================================================//
	$('.search-open').on('click', function() {
		$('.nav-search-top').toggleClass('height');
	});

// FAQ open ===============================================================//

	$('.question').click(function () {
		var el = $(this).next(),
		curHeight = el.height(),
		autoHeight = el.css('height', 'auto').height();
		el.height(curHeight).animate({
			height: autoHeight == curHeight ? "0" : autoHeight
		}, 500);
	});

	$('.question').click(function(){
			$(this).toggleClass('rotate-after');
	});

//toggle list to show blog listing ===============================================================//
	$('.toggle-list-close').click(function(){
		$('.toggle-list-close').toggleClass('show');
			$('.sticky-listing li').toggleClass('show');
	});

//toggle horizontal filters=======================================================================//

	$('.show-filter').click(function(){
			$('.hide-filters').toggleClass('show');
	});

	$('.horizontal-filters li span').click(function(){
		$(this).parent().toggleClass('filter-selected');
	});

	$('.horizontal-filters li span').click(function(){
		$(this).siblings().toggleClass('show');
	});

	$('.horizontal-filters ul li ').click(function(){
			$(this).toggleClass('selected-filter');
	});

//show horizontal filters with styling===========================================================//
	$('.filter-select').each(function(){
		var $self = $(this);
		var $form = $self.closest('form').addClass('enhanced');

		var $select = $('select', $self);
		var $options = $('option', $select);
		var $label = $('span', $self);

		var $dynamicLabel = $label;
		var $optionList = $('<ul></ul>');

		$select.hide();

		var setDynamicLabel = function(){
			var $selectedItem = $('li.selected', $optionList);
			var data = String($selectedItem.data('val'));

						$dynamicLabel.html($selectedItem.text());   // todo: strip the span out of this
						$self.addClass('active');
		};

		// append after select
		$select.after($dynamicLabel, $optionList);

		/* create html of options from existing select options */
		var newOptions = '';
		$options.each(function(){
			var isSelected = $(this).prop('selected') == true ? "selected" : "";

			$optionList.append('<li data-val="' + ($(this).attr('value') ? $(this).val() : "") + '" class="'+ isSelected +'"><span>' + $(this).html() + '</span></li>');
		});

		setDynamicLabel();

		/* Change label values when options are chosen */
		$('li', $optionList).on('click keydown', function(){
			$(this).siblings().removeClass('selected');
			$(this).addClass('selected');

			setDynamicLabel();

			$select.val($(this).data('val'));
		});
	});

//tab-process-content ==========================================================================//
	$('.first-tab-toggle').click(function(){
		$('.first-tab-toggle').addClass('active');
		$('.first-tab').addClass('active');
		$('.second-tab').removeClass('active');
		$('.second-tab-toggle').removeClass('active');
	});

	$('.second-tab-toggle').click(function(){
		$('.second-tab-toggle').addClass('active');
		$('.second-tab').addClass('active');
		$('.first-tab').removeClass('active');
		$('.first-tab-toggle').removeClass('active');
	});


//feedback=====================================================================================//
	$( '.feedback .click' ).on( 'click', function(){
		var $item = $(this);
		$item.addClass( 'animate' );
		setTimeout(function(){
			$item.removeClass( 'animate' );
		}, 500)
	});

//sticky ======================================================================================//
	setTimeout(sloooow, 100);

	function sloooow() {

			var stickEl = $('.sticky');

				if (stickEl.length) {
						stickyElTop = stickEl.offset().top;

						var sticky = function(){
								var scrollTop = $(window).scrollTop();

								if (stickyElTop < scrollTop+20) {
									// Detect width and enforce it when element becomes sticky,
									// rather than trying to calculate it with CSS.
									var currentWidth = stickEl.width();
										stickEl.addClass('is-fixed').css('width', currentWidth);
								} else {
										stickEl.removeClass('is-fixed').removeAttr('style');
								}
						};

						$(window).scroll(function() {
								sticky();
						});
				}
		}

//Search focus=====================================================================================//
	$( '.search' ).on( 'click', function(){
		 $(document.search.query).focus();
	});


//Equal Heigths=====================================================================================//
		var equalHeightColumns = [
				'.js-equal-height-body-left-col',
				'.js-equal-height-body-right-col'
		];

		var makeEqualHeight = function(cols) {

				var tallest = cols.sort(function (a, b) {
						return $(a).outerHeight() < $(b).outerHeight() ? 1 : -1;
				})[0];

				for (var i = 0; i < cols.length; i++) {
						$(cols[i]).outerHeight($(tallest).height());
				}
		};

		makeEqualHeight(equalHeightColumns);

		$( window ).resize(function() {
				makeEqualHeight(equalHeightColumns);
		});

		var socialShare = function(){

				var $document       = $( document ),
						$shareBar       = $( '.social-sharebar' ),
						$shareButton    = $shareBar.find( '.social-sharebar__button' ),
						$shareIcons     = $shareBar.find( '.social-sharebar__icons' ),
						shareBarFixed   = 'social-sharebar--fixed',
						hideButton      = 'social-sharebar__button--hidden',
						showIcons       = 'social-sharebar__icons--visible',
						offset          = 130;

				$document.on( 'scroll load', function () {
						if ( $document.scrollTop() >= offset ) {
								$shareBar.addClass( shareBarFixed );
						} else {
								$shareBar.removeClass( shareBarFixed );
						}
				});

				$shareBar.on( 'mouseenter', function () {
						$shareButton.addClass( hideButton );

						setTimeout(function() {
								$shareIcons.addClass( showIcons );
						}, 100);
				});

				$shareBar.on( 'mouseleave', function () {
						$shareButton.removeClass( hideButton );
						$shareIcons.removeClass( showIcons );
				});
		}

		socialShare();
});
