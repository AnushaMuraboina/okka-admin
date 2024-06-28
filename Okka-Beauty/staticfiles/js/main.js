$(document).ready(function () {
  $('.my-slider').slick({
    slidesToShow: 5,
    slidesToScroll: 5,
    arrows: true,
    dots: true,
    speed: 300,
    infinite: true,
    autoplaySpeed: 10000,
    autoplay: true,
    responsive: [
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  });
});


//for tooltip
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})


$(document).ready(function () {
  $('.my-slider-1').slick({
    slidesToShow: 5,
    slidesToScroll: 5,
    arrows: true,
    dots: true,
    speed: 300,
    infinite: true,
    autoplaySpeed: 5000,
    autoplay: true,
    responsive: [
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  });
});


$(document).ready(function () {
  $('.my-slider-3').slick({
    slidesToShow: 7,
    slidesToScroll: 7,
    arrows: true,
    dots: true,
    speed: 300,
    infinite: true,
    autoplaySpeed: 5000,
    autoplay: true,
    responsive: [
      {
        breakpoint: 1100,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  });
});

$(document).ready(function () {
  $('.my-slider-4').slick({
    slidesToShow: 4,
    slidesToScroll: 4,
    arrows: true,
    dots: true,
    speed: 300,
    infinite: true,
    autoplaySpeed: 5000,
    autoplay: true,
    responsive: [
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  });
});


$(document).ready(function () {
  $('.my-slider-8').slick({
    slidesToShow: 5,
    slidesToScroll: 5,
    arrows: true,
    dots: true,
    speed: 300,
    infinite: true,
    autoplaySpeed: 5000,
    autoplay: true,
    responsive: [
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 2,
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  });
});





$(document).ready(function () {
  $('.my-slider-details').slick({
    slidesToShow: 4,
    slidesToScroll: 4,
    arrows: true,
    dots: true,
    speed: 300,
    infinite: true,
    autoplaySpeed: 5000,
    autoplay: true,
    responsive: [
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  });
});



$(document).ready(function () {
  $('.my-slider-6').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    dots: true,
    speed: 300,
    infinite: true,
    autoplaySpeed: 5000,
    autoplay: true,
    responsive: [
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  });
});


// increment

// $(document).ready(function () {
//   var slider = $("#slider");
//   var thumb = $("#thumb");

//   function syncPosition(el) {
//     var count = el.item.count - 1;
//     var current = Math.round(el.item.index - (el.item.count / 2) - .5);
//     if (current < 0) {
//       current = count;
//     }
//     if (current > count) {
//       current = 0;
//     }
//     thumb
//       .find(".owl-item")
//       .removeClass("current")
//       .eq(current)
//       .addClass("current");
//     var onscreen = thumb.find('.owl-item.active').length - 1;
//     var start = thumb.find('.owl-item.active').first().index();
//     var end = thumb.find('.owl-item.active').last().index();
//     if (current > end) {
//       thumb.data('owl.carousel').to(current, 100, true);
//     }
//     if (current < start) {
//       thumb.data('owl.carousel').to(current - onscreen, 100, true);
//     }
//   }
//   function syncPosition2(el) {
//     if (syncedSecondary) {
//       var number = el.item.index;
//       slider.data('owl.carousel').to(number, 100, true);
//     }
//   }
//   thumb.on("click", ".owl-item", function (e) {
//     e.preventDefault();
//     var number = $(this).index();
//     slider.data('owl.carousel').to(number, 300, true);
//   });


//   $(".qtyminus").on("click", function () {
//     var now = $(".qty").val();
//     if ($.isNumeric(now)) {
//       if (parseInt(now) - 1 > 0) { now--; }
//       $(".qty").val(now);
//     }
//   })
//   $(".qtyplus").on("click", function () {
//     var now = $(".qty").val();
//     if ($.isNumeric(now)) {
//       $(".qty").val(parseInt(now) + 1);
//     }
//   });
// });



//for the wishlist radio button
// function wish_myFunction() {
//   var checkBox = document.getElementById("wish-myCheck");
//   var text_wishlist = document.getElementById("text-cart-whishlist");
//   if (checkBox.checked == true) {
//     text_wishlist.style.display = "block";
//   } else {
//     text_wishlist.style.display = "none";
//   }
// }


