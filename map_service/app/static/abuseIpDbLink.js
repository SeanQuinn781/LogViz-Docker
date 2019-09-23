export function abuseIpDbLink(abuseIpDbBaseLink) {
  let abuseIpDbLink = $('<a></a>')
    .attr('href', abuseIpDbBaseLink)
    .text('Abuse IP DB')
    .attr('target','_blank')
    .addClass('abuseIpDbLink');
  return abuseIpDbLink[0];
}