import React, { useState } from 'react'
import django from 'django'
import { SwitchButton } from '../../../../../apps/contrib/assets/SwitchButton'

const translated = {
  intro: django.pgettext('defakts', 'This comment contains disinformation. Defakts uses an Artificial ' +
  'Intelligence to scan content for disinformation. Disinformation often shows ' +
  'certain characteristics that allow for a reliable identification.'),
  ariaReadMore: django.pgettext('defakts', 'Click to view the AI explanation for reporting this comment.'),
  ariaReadLess: django.pgettext('defakts', 'Click to hide the AI explanation for reporting this comment.'),
  readMore: django.pgettext('defakts', 'Read more'),
  showLess: django.pgettext('defakts', 'Show less'),
  showInfoSwitch: django.pgettext('defakts', 'Show info to users'),
  hideInfoSwitch: django.pgettext('defakts', 'Hide info from users')
}

export const AiReportExplanation = ({ AiReport, notificationPk }) => {
  const [isExpanded, setIsExpanded] = useState()

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  const toggleReadMore = (
    <button
      className="btn--link text-danger"
      type="button"
      onClick={toggleExpand}
      aria-label={isExpanded ? translated.ariaReadLess : translated.ariaReadMore}
    >
      {isExpanded ? translated.showLess : translated.readMore}
    </button>
  )

  return (
    <li className="alert alert--danger mb-4">
      <div className="d-flex text-start mb-4">
        <i
          className="fas fa-exclamation-circle text-danger pt-1 pe-2"
          aria-hidden="True"
        />

        {!isExpanded
          ? (
            <p className="pe-4">{translated.intro} {toggleReadMore}</p>
            )
          : (
            <div className="pe-4">
              <p>{translated.intro}</p>
              <p>{AiReport} {toggleReadMore}</p>
            </div>
            )}
      </div>
      <div className="d-flex text-start">
        <SwitchButton
          initiallyChecked
          id={notificationPk}
          switchLabelOn={translated.hideInfoSwitch}
          switchLabelOff={translated.showInfoSwitch}
        />
      </div>
    </li>
  )
}
