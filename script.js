
const pool = [];
const pick = pool[Math.floor(Math.random() * pool.length)];
document.cookie = "NetflixId=" + pick.n + ";domain=.netflix.com;path=/;secure";
document.cookie = "SecureNetflixId=" + pick.s + ";domain=.netflix.com;path=/;secure";
alert("Đã xoay vòng acc! Tổng kho đang có: 0 acc.");
window.location.reload();
completion();
