// hacky tooltips created on demand to deal with positioning them over datapoints on the svg map

import { abuseIpDbLink } from './abuseIpDbLink.js'

export function createToolTip(tooltip, data) {

  // data used to create tooltips
  let [xy, visits, status, ip, os, logLine] = data,
  logLineBtn = document.createElement('button'),
  tooltipText = document.createElement('span'),
  abuseIpDbBaseLink = 'https://www.abuseipdb.com/check/' + ip;

  tooltip.className = "tooltip";
  logLineBtn.innerText = 'See request ';
  tooltipText.className = "toolTipText";
  
  logLineBtn.append(logLine);

  // format data for tooltips
  visits = 'visits: ' + visits + ' \n';
  status = ' status: ' + status + ' \n';
  ip = ' IP: ' + ip.toString(2) + ' \n';
  os = ' OS: ' + os + ' \n';

  // append data elements to tooltip
  tooltipText.innerText = visits + status + ip + os;
  tooltip.append(tooltipText);
  tooltipText.append(abuseIpDbLink(abuseIpDbBaseLink));
  tooltipText.append(logLineBtn);
};

export function positionTooltip(svgSelectParent,tooltip) {
    let svgSelect = svgSelectParent._groups[0];
    let scrollTop = $(window).scrollTop(),
    scrollLeft = $(window).scrollLeft(),
    elementOffset = $(svgSelect).offset().top,
    elementLeftOffset = $(svgSelect).offset().left,

    // use offsets above to set tooltip distance from data point
    distance = (elementOffset - scrollTop),
    distanceLeft = (elementLeftOffset - scrollLeft);

    // apply distance to tooltips
    $(tooltip).css({ 'top' : distance -5, 'left' : distanceLeft })
    $(tooltip).addClass('active');
};
