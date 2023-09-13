import React from 'react'
import django from 'django'
import Slider from 'react-slick'

const translated = {
  userReport: django.pgettext('defakts', 'User {}username{} reported the comment and gave this reason:')
}

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

  function getUsername (string, userName) {
    const splitted = string.split('{}')
    return (
      <p>
        {splitted[0]}
        <b>{userName}</b>
        {splitted[2]}
      </p>
    )
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
            <div className="poll-slider__answer">
              {getUsername(translated.userReport, slide.username)}
              <p className={'fs-6 ' + (props.userReport.length > 1 ? '' : 'mb-0')}>"{slide.description}"</p>
            </div>
            <div className={props.userReport.length > 1 ? 'poll-slider__count--spaced' : 'poll-slider__count'}>
              {index + 1}/{props.userReport.length}
            </div>
          </div>
        ))}
      </Slider>
    </li>
  )
}
