import React from 'react'
import Slider from 'react-slick'

export const UserReport = (props) => {
  const settings = {
    arrows: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    className: props.sliderClass,
    infinite: false,
    centerMode: true,
    centerPadding: '0px'
  }

  return (
    <li className="alert alert--danger pb-0">
      <Slider {...settings}>
        {props.userReport.map((slide, index) => (
          <div
            className="px-4"
            data-index={index}
            key={index}
          >
            <p className="poll-slider__answer">
              {slide}
            </p>
            <div className={props.userReport.length > 1 ? 'poll-slider__count--spaced' : 'poll-slider__count'}>
              {index + 1}/{props.userReport.length}
            </div>
          </div>
        ))}
      </Slider>
    </li>
  )
}
