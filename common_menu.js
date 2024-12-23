menu_sets = []
//메뉴 생성기 시작 $================================

class Menu{
    constructor(mtitle){
        this.mtitle = mtitle;
        this.url;
        this.tips;
    }
}
menu1 = new Menu("CNN AND CRAWLING");
menu1.url = "https://human4255.github.io/classification_model/";
menu1.tips = "구글,네이버 이미지 크롤링 및 컨볼루션 적용한";
menu2 = new Menu("TEST MENU");
menu2.url = "https://human4255.github.io/classification_model/";
menu2.tips = "테스트용";

menu_sets.push(menu1)
menu_sets.push(menu2)
//메뉴 생성기 종료 $================================