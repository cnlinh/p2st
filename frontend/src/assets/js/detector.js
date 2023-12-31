import utils from './utils';
/* -------------------------------------------------------------------------- */
/*                                  Detector                                  */
/* -------------------------------------------------------------------------- */

const detectorInit = () => {
  const { is } = window;
  const html = document.querySelector('html');

  is.opera() && utils.addClass(html, 'opera');
  is.mobile() && utils.addClass(html, 'mobile');
  is.firefox() && utils.addClass(html, 'firefox');
  is.safari() && utils.addClass(html, 'safari');
  is.ios() && utils.addClass(html, 'ios');
  is.iphone() && utils.addClass(html, 'iphone');
  is.ipad() && utils.addClass(html, 'ipad');
  is.ie() && utils.addClass(html, 'ie');
  is.edge() && utils.addClass(html, 'edge');
  is.chrome() && utils.addClass(html, 'chrome');
  is.mac() && utils.addClass(html, 'osx');
  is.windows() && utils.addClass(html, 'windows');
  navigator.userAgent.match('CriOS') && utils.addClass(html, 'chrome');
};

export default detectorInit;
