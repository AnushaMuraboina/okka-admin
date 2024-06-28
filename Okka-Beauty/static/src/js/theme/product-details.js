/* eslint-disable no-new */
/*-----------------------------------------------
|                    Swiper
-----------------------------------------------*/

const getThubmnailDirection = () => {
  if (
    window.innerWidth < 768 ||
    (window.innerWidth >= 992 && window.innerWidth < 1200)
  ) {
    return 'horizontal';
  }
  return 'vertical';
};

const productDetailsInit = () => {
  const { getData, resize } = window.phoenix.utils;
  const productDetailsEl = document.querySelector('[data-product-details]');
  if (productDetailsEl) {
    const colorVariantEl = productDetailsEl.querySelector(
      '[data-product-color]'
    );
    const productQuantityEl = productDetailsEl.querySelector(
      '[data-product-quantity]'
    );
    const productQuantityInputEl = productDetailsEl.querySelector(
      '[data-quantity] input[type="number"]'
    );
    const productColorVariantConatiner = productDetailsEl.querySelector(
      '[data-product-color-variants]'
    );

    const swiperInit = productImages => {
      const productSwiper = productDetailsEl.querySelector(
        '[data-products-swiper]'
      );

      const options = getData(productSwiper, 'swiper');

      const thumbTarget = getData(productSwiper, 'thumb-target');

      const thumbEl = document.getElementById(thumbTarget);

      let slides = '';
      productImages.forEach(img => {
        if (img.type === 'video/mp4') {
          slides += `
            <div class='swiper-slide'>
              <video class='w-100' controls>
                <source src=${img.url} type='video/mp4'>
                Your browser does not support the video tag.
              </video>
            </div>
          `;
        } else {
          slides += `
            <div class='swiper-slide'>
              <img class='w-100 zoom' src=${img} data-zoom-image=${img} alt='product-image'>
            </div>
          `;
        }
      productSwiper.innerHTML = `<div class='swiper-wrapper'>${slides}</div>`;

      let thumbSlides = '';
      productImages.forEach(img => {
        if (img.type === 'video/mp4') {
          thumbSlides += `
            <div class='swiper-slide'>
              <div class='product-thumb-container p-2 p-sm-3 p-xl-2 bg-white'>
                <video controls>
                  <source src=${img.url} type='video/mp4'>
                  Your browser does not support the video tag.
                </video>
              </div>
            </div>
          `;
        } else {
          thumbSlides += `
            <div class='swiper-slide'>
              <div class='product-thumb-container p-2 p-sm-3 p-xl-2 bg-white'>
                <img src=${img} data-zoom=${img} alt='product-image'>
              </div>
            </div>
          `;
        }
      });
      thumbEl.innerHTML = `<div class='swiper-wrapper'>${thumbSlides}</div>`;

      const thumbSwiper = new window.Swiper(thumbEl, {
        slidesPerView: 5,
        spaceBetween: 16,
        direction: getThubmnailDirection(),
        breakpoints: {
          768: {
            spaceBetween: 100
          },
          992: {
            spaceBetween: 16
          }
        }
      });

      const swiperNav = productSwiper.querySelector('.swiper-nav');

      resize(() => {
        thumbSwiper.changeDirection(getThubmnailDirection());
      });

      new Swiper(productSwiper, {
        ...options,
        navigation: {
          nextEl: swiperNav?.querySelector('.swiper-button-next'),
          prevEl: swiperNav?.querySelector('.swiper-button-prev')
        },
        thumbs: {
          swiper: thumbSwiper
        }
      });
    };

    const colorVariants =
      productColorVariantConatiner.querySelectorAll('[data-variant]');

    colorVariants.forEach(variant => {
      if (variant.classList.contains('active')) {
        swiperInit(getData(variant, 'products-images'));
        colorVariantEl.innerHTML = getData(variant, 'variant');
      }
      const productImages = getData(variant, 'products-images');

      variant.addEventListener('click', () => {
        swiperInit(productImages);
        colorVariants.forEach(colorVariant => {
          colorVariant.classList.remove('active');
        });
        variant.classList.add('active');
        colorVariantEl.innerHTML = getData(variant, 'variant');
      });
    });
    productQuantityInputEl.addEventListener('change', e => {
      if (e.target.value == '') {
        e.target.value = 0;
      }
    });
  }
};

export default productDetailsInit;
