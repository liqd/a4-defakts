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
  readLess: django.pgettext('defakts', 'Read less'),
  showInfoSwitch: django.pgettext('defakts', 'Show info to users'),
  hideInfoSwitch: django.pgettext('defakts', 'Hide info from users')
}

export const AiReportExplanation = ({ AiReport, notificationPk }) => {
  const [isExpanded, setIsExpanded] = useState()

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  return (
    <li className="alert alert--danger mb-4">
      <div className="d-flex text-start mb-4">
        <i
          className="fas fa-exclamation-circle text-danger pt-1 pe-2"
          aria-hidden="True"
        />
        <p className="pe-4">
          {translated.intro + ' '}
          {isExpanded && AiReport + ' '}
          <button
            className="btn--link text-danger"
            type="button"
            onClick={toggleExpand}
            aria-label={isExpanded ? translated.ariaReadLess : translated.ariaReadMore}
          >
            {isExpanded ? translated.readLess : translated.readMore}
          </button>
        </p>
      </div>
      <div className="d-flex text-start">
        <SwitchButton
          id={notificationPk}
          switchLabelOn={translated.hideInfoSwitch}
          switchLabelOff={translated.showInfoSwitch}
        />
      </div>
    </li>
  )
}
