/*
 * D&D 九宫格阵营测试
 * - 纯前端计算，不存储、不发送答案
 * - 题目与计分逻辑据文末署名来源整理
 * - 仅在包含 #dnd-alignment-app 的页面激活
 */
(function () {
  "use strict";

  const SECTIONS = [
    {
      title: "第一卷：对亲戚的看法",
      questions: [
        ["长辈在家族中公开反对你，你会：", [
          ["接受批评，改变方法", "xg", 2],
          ["尝试与长辈妥协，用折衷的方法", "xg", 1],
          ["忽略长辈的轻蔑，诽谤他们", "xe", 1],
          ["千方百计使他们收声", "xe", 2]
        ]],
        ["你会放弃一个前途无量的职业来帮忙解决家庭的燃眉之急吗？", [
          ["不用想，肯定会", "xg", 2],
          ["会，但有点不情愿", "xg", 1],
          ["除非我肯定自己会很快重回工作岗位", "xn", 1],
          ["不会", "xn", 2]
        ]],
        ["你会为了前途而背叛家人吗？", [
          ["会，不带一点罪恶感", "xe", 2],
          ["会——只要我能秘密行事", "xe", 1],
          ["我会抗拒这份诱惑", "xn", 1],
          ["我认为这个主意极为可恨", "xn", 2]
        ]],
        ["你尊敬一家之主吗？", [
          ["他们的言语指导着我的行动", "lx", 2],
          ["他们是我的榜样", "lx", 1],
          ["他们通常与我无关", "cx", 1],
          ["我当他们透明", "cx", 2]
        ]],
        ["如果家族要你与一个令人作呕的家伙结婚，你会：", [
          ["听从安排，为能帮助家族而自豪", "lx", 2],
          ["会，但强颜欢笑", "lx", 1],
          ["巧妙地抗婚", "nx", 1],
          ["逃跑", "nx", 2]
        ]],
        ["有一位家人疏远了你。在他弥留之际，他想与你和解。你会：", [
          ["与他谈谈，但坚守立场", "cx", 2],
          ["不跟他说话", "cx", 1],
          ["不计前嫌，敞开心扉地讨论前事", "nx", 1],
          ["积极进行和解，并留心听他的遗言", "nx", 2]
        ]]
      ]
    },
    {
      title: "第二卷：对朋友的看法",
      questions: [
        ["一位位高权重的腐败法官允诺：如果你作出对朋友不利的假证，就给你一大笔钱。你会：", [
          ["照做，然后拿钱", "xe", 2],
          ["拿钱照做，但尽量使证词显得无力", "xe", 1],
          ["拒绝", "xg", 1],
          ["不管结果如何，都站在朋友那一边", "xg", 2]
        ]],
        ["你会亲近朋友，还是与大部分人保持距离以保安全？", [
          ["我有一大群密友", "xg", 2],
          ["我有一些密友", "xg", 1],
          ["我有几个密友", "xn", 1],
          ["我会与人保持距离", "xn", 2]
        ]],
        ["你背叛过朋友吗？", [
          ["我干过不止一次，有时也能逃避惩罚", "xe", 2],
          ["我只干过那么一次", "xe", 1],
          ["我曾被怂恿过这么做，但从未做过", "xn", 1],
          ["我从未考虑过这种事", "xn", 2]
        ]],
        ["你怎么看待“执子之手，与子偕老”这类对爱人的终生承诺？", [
          ["我曾有过或正渴望着这么一段关系", "lx", 2],
          ["这种关系挺理想的——如果能成功的话", "lx", 1],
          ["我担心自己会错过其他人对我的爱", "cx", 1],
          ["作茧自缚？真是天大的错误", "cx", 2]
        ]],
        ["朋友借了你钱，你会要求他们归还吗？", [
          ["会，而且写好借据，不得抵赖", "lx", 2],
          ["会，但期限上会宽松些", "lx", 1],
          ["不会，尽管还了会更好", "nx", 1],
          ["不会，他们欠我一个人情", "nx", 2]
        ]],
        ["你仍与儿时玩伴保持联络吗？", [
          ["是的，我们定期通信", "nx", 2],
          ["是的，我们努力保持联络", "nx", 1],
          ["不会，我经常搬家", "cx", 1],
          ["不会，我不再与他们有共同之处", "cx", 2]
        ]]
      ]
    },
    {
      title: "第三卷：对集体的看法",
      questions: [
        ["你会花时间和金钱在集体上吗？", [
          ["会，我会优先考虑集体的需要", "xg", 2],
          ["如果我的需求被满足，我会尽我所能", "xg", 1],
          ["不会，我没钱也不闲", "xn", 1],
          ["不会，花时间和金钱在集体上是一种浪费", "xn", 2]
        ]],
        ["集体面临被侵害的威胁，你会：", [
          ["保卫它直至自己的最后一口气", "xg", 2],
          ["和残存同伴构筑防御", "xg", 1],
          ["一看到势头不对就逃跑", "xe", 1],
          ["与入侵者达成协议，成为间谍", "xe", 2]
        ]],
        ["如果你受伤了，需要急救，你的同伴愿意帮助你吗？", [
          ["会，因为他们知道我也会为他们做同样的事", "xn", 2],
          ["会，因为我很受欢迎", "xn", 1],
          ["可能不会，因为我不受信任", "xe", 1],
          ["肯定不会，我在集体中树敌了", "xe", 2]
        ]],
        ["你尊重集体的规章和领袖吗？", [
          ["毋庸置疑，是的", "lx", 2],
          ["是的，总的来说它们是最佳的管理方式", "lx", 1],
          ["当它适合我时，我才会——有些规章我并不认同", "cx", 1],
          ["我不关心它们；它们拿我没辙", "cx", 2]
        ]],
        ["同伴回避你，或嘲笑你吗？", [
          ["是的，这些井底之蛙不会理解超规格的人", "cx", 2],
          ["有些会，因为并不是所有人都认同我", "cx", 1],
          ["不会，我看起来一切正常", "nx", 1],
          ["不会，我就是集体中正常人的标准", "nx", 2]
        ]],
        ["你当官会为民作主，或者希望代表集体的意志吗？", [
          ["做这种事是我所乐意接受的荣誉", "lx", 2],
          ["当然，这是每个人的义务", "lx", 1],
          ["不会，除非无人能接手此事", "nx", 1],
          ["不会，我不想为集体利益负责", "nx", 2]
        ]]
      ]
    },
    {
      title: "第四卷：对国家的看法",
      questions: [
        ["你的国家闹饥荒，你会：", [
          ["与其他人共享自己有的食物", "xg", 2],
          ["自己吃尽可能少，余下的给其他人", "xg", 1],
          ["偷取自己生存所需的食物", "xe", 1],
          ["偷取尽可能多的食物，然后高价卖出", "xe", 2]
        ]],
        ["给你足够的钱，你会往国王的酒中下毒吗？", [
          ["会，类似的事我干过", "xe", 2],
          ["如果能逃避惩罚，我会", "xe", 1],
          ["不会，尽管这一大笔钱很诱人", "xn", 1],
          ["不会，而且我会提醒国王小心这个阴谋", "xn", 2]
        ]],
        ["瘟疫传遍你的国家，你会：", [
          ["接下寻找解药的危险任务", "xg", 2],
          ["尽力治好病人", "xg", 1],
          ["避免接触病人", "xn", 1],
          ["逃离国家", "xn", 2]
        ]],
        ["你尊重领主的法律权威吗？", [
          ["是的，领主万岁！", "lx", 2],
          ["是的，我们的统治者大体上公平、公正", "lx", 1],
          ["不会，统治者也只是普通人", "cx", 1],
          ["不会，权力必定导致腐化", "cx", 2]
        ]],
        ["给你一笔稳赚的生意，你会为敌国做间谍吗？", [
          ["会，因为我的国家势必任人鱼肉", "cx", 2],
          ["会，因为国家机密对我无关紧要", "cx", 1],
          ["不会，我会被抓", "nx", 1],
          ["不会，我不会辜负国家对我的信任", "nx", 2]
        ]],
        ["你依靠政府来建立社会契约和保障所有权吗？", [
          ["是的，因为维护法律比任何个人争执都重要", "lx", 2],
          ["是的，因为法庭就是为解决这种争执而设立的", "lx", 1],
          ["你在开玩笑吗？政府连路都不会铺", "nx", 1],
          ["绝对不会；如果我不能自己保护财产，就无权拥有它", "nx", 2]
        ]]
      ]
    },
    {
      title: "第五卷：对刑罚的看法",
      questions: [
        ["如果你入狱了，你会伤害或杀死其他人来脱狱吗？", [
          ["会，服刑这么多年等于锁住自己", "xe", 2],
          ["会，在犯事时便已知道这风险", "xe", 1],
          ["不会，除非只造成容易愈合的小伤", "xn", 1],
          ["不会，那些守卫只是在尽本分", "xn", 2]
        ]],
        ["你接受贵族有权恶劣对待手下的仆人吗？", [
          ["是的，贵族们只是幸运地投了个好胎", "xn", 2],
          ["是的，有时要靠吓，他们才肯干活", "xn", 1],
          ["不会，贵族应仁慈地统治", "xg", 1],
          ["任何人都无权恶劣对待别人", "xg", 2]
        ]],
        ["你意外地犯罪了，你会：", [
          ["认罪，并向受害者赔偿", "xg", 2],
          ["认罪，向法官请求宽大处理", "xg", 1],
          ["隐瞒自己的涉案事实，必要时说谎", "xe", 1],
          ["嫁祸于人", "xe", 2]
        ]],
        ["如果犯罪了，你会认罪吗？", [
          ["会，因为我有这个责任", "lx", 2],
          ["会，因为我会因此获得轻判", "lx", 1],
          ["不会，我会等检察官证明我有罪", "nx", 1],
          ["不会，我会证明自己“无罪”", "nx", 2]
        ]],
        ["如果可能被惩罚，你会表明一个革命性的政见吗？", [
          ["会，我宁愿受罚也不愿保持沉默", "cx", 2],
          ["会，总要有人说真话", "cx", 1],
          ["不会，尽管私下会对朋友说", "nx", 1],
          ["不会，不值得为政治费神", "nx", 2]
        ]],
        ["旅行时，你目击了一场袭击。你被传去作证，这会非常耽误行程。你会：", [
          ["连夜溜走，避免作证", "cx", 2],
          ["说自己什么也没看到", "cx", 1],
          ["勉强留下，作证，然后离开", "lx", 1],
          ["留下直至结案所需证供足够", "lx", 2]
        ]]
      ]
    },
    {
      title: "第六卷：对财富的看法",
      questions: [
        ["财富的最大用途是什么？", [
          ["帮助穷人和不幸的人", "xg", 2],
          ["满足亲朋好友的需要", "xg", 1],
          ["让自己达到人生巅峰", "xe", 1],
          ["不仅达到巅峰，还要阻止别人超过自己", "xe", 2]
        ]],
        ["遇到乞丐，你会：", [
          ["慷慨地给钱", "xg", 2],
          ["恰到好处地给钱", "xg", 1],
          ["只给自己认为无所谓的钱——至多一两块", "xn", 1],
          ["视而不见", "xn", 2]
        ]],
        ["通过魔法，你可以使村里的商人以为你的铜币是金币。你会这样做吗？", [
          ["会，而且还要尽可能地消费", "xe", 2],
          ["会，但只骗富商", "xe", 1],
          ["不会，风险太大", "xn", 1],
          ["不会，商人也要养家糊口", "xn", 2]
        ]],
        ["你有两份工作可选：一份酬劳更多，另一份较稳定。你会选哪一份？", [
          ["肯定是更赚钱的；稳定的工作听上去像苦差事", "nx", 2],
          ["可能是前者，尽管我会看看后者做些什么", "nx", 1],
          ["后者，除非前者赚的钱多到吓人", "lx", 1],
          ["肯定是稳定的，因为我有长远计划", "lx", 2]
        ]],
        ["最佳的致富途径是什么？", [
          ["这关乎天时地利，还有一时运气", "cx", 2],
          ["灵活变通会带来更多机会", "cx", 1],
          ["按照一个有适度风险的长期计划来做", "lx", 1],
          ["努力工作，坚持不懈", "lx", 2]
        ]],
        ["如果你接手一项工作，尽管它会很危险，你会努力完成吗？", [
          ["会，我说话算数", "nx", 2],
          ["会，因为别人会认为我信得过，这很好", "nx", 1],
          ["你可以赌我会不会爽约", "cx", 1],
          ["如果这不是什么好差事，那算了", "cx", 2]
        ]]
      ]
    }
  ];

  const ALIGNMENTS = {
    lg: {
      name: "守序善良",
      english: "Lawful Good",
      description: "守序善良的人物相信，规律而强大的社会和高尚的政府，可以让大多数人民生活得更好。只要人们相信法律，并试着互相帮助，整个社会就将因此而进步。因此，这个阵营的人物将会朝着这个方向努力，他们会尽可能地为大多数人带来较多的福利及较少的伤害。他们必定信守自己的承诺。守序善良的人物，特别是圣武士，时常自己陷于善良与法律相冲突的两难处境。比如履行誓言可能会伤及无辜时，或在宗教法规和地方法律相矛盾时。"
    },
    ng: {
      name: "中立善良",
      english: "Neutral Good",
      description: "中立善良的人物相信力量平衡是十分重要的事，单方面地强调秩序或混乱，是无法达到至善的。因为整个宇宙中充满了朝着各式各样的目标而努力的生物，所以若要追求至善，便不能破坏这种平衡，甚至的设法维持这种平衡，如果说支持社会秩序可以带来至善，便得以为之。若推翻既有的社会秩序就可以达到至善，那也必须为之。社会结构对他们来说，没什么重大意义。中立善良的长处是，行善不为阶级偏见所影响。"
    },
    cg: {
      name: "混乱善良",
      english: "Chaotic Good",
      description: "混乱善良的人物虽然喜欢按照自己的意思行事，心地却不错。尽管他们认同一切美德和公理，却不愿意受到律法和规范的约束。想要任意驱使这些人，要他们遵照命令做事是不可能的。这些人有自己的一套道德标准，虽然不至于为恶，但也不见得和一般大众的道德标准完全相同。混乱善良人物常会因为感到受人指使而在团队内制造矛盾，比起有计划的行动他们更喜欢即兴发挥。混乱善良阵营的人物不介意用恶毒的手段制裁他们认为是邪恶的人，即便并不喜欢这样做，但他们本身却并不带有恶意。"
    },
    ln: {
      name: "守序中立",
      english: "Lawful Neutral",
      description: "守序中立的人物而言，秩序和组织是非常重要的。他们认同强大、井然有序的统治阶层，不管这个统治阶层是专制的暴君，还是安和乐利的民主政府，这些人都不在乎，世界上必须有法律，而法律则必须被遵守。对他们而言，绝对的秩序比什么道德良知来的重要。只要是规定，不管结果是好是坏，都必须遵行无误。绝对公正的法官，和绝对服从命令的士兵，都是此阵营的最佳典范。守序中立对善恶持中立态度，但这不代表他们是不道德的、是道德虚无主义者或是没有道德立场。他们只不过是将道德观念永远置于服从信条、传统或者法律之下。他们通常有强烈的伦理信条，但这一信条是首先基于其信念体系，而非基于善恶认同。"
    },
    nn: {
      name: "绝对中立",
      english: "True Neutral",
      description: "绝对中立的人物相信绝对平衡的力量，因此，他们拒绝采取任何被视为邪恶和暴力的行动。绝对中立的人会尽力避免和善良或邪恶，秩序或叛逆的力量合流。有时候他们发现自己被迫得和某个阵营结盟。为了保持平衡，这些人会刻意改变立场，和弱势者合作。然而，当强弱势力对换时，他们也会毫不犹豫地跟着改变立场。"
    },
    cn: {
      name: "混乱中立",
      english: "Chaotic Neutral",
      description: "混乱中立的人按自己一时的兴致行动。他是一个完全的个人主义者。他重视自己的自由权利，但并不致力于保护别人的自由。他蔑视权威，愤恨约束并且挑战传统。混乱中立者并不会向无政府运动那样有意瓦解组织。如果这么做，他必须把自己的阵营转成善良(希望解放他人)或是邪恶(使异己受苦)。混乱中立的寻常称谓是“真正混乱”。注意，混乱中立者的行为也许很难预测，但他的举止并非完全随机的，他从桥上的走过去的可能性和从桥上跳下去的可能性大小并不相等。混乱中立是一个真正自由于社会约束和对改良社会的空想的阵营。"
    },
    le: {
      name: "守序邪恶",
      english: "Lawful Evil",
      description: "守序邪恶的人有系统地得到他想要的东西，此行为受到他行为准则的限制，但并不顾及受其伤害的人。他关心传统、忠诚和秩序，但不关心自由、尊严和生命。他按规则行动，但没有怜悯和同情。他觉得待在统治阶层里很舒服，愿意支配别人，但也乐意为别人服务。他处罚谴责别人并不是根据他们的行为而是根据种族、信仰、祖国或社会阶层。他不愿违反法律或承诺，这种不愿部分是因为他的天性，部分是因为他需要秩序来保护他免受道德上的反对。某些守序邪恶者有特别的禁忌，比如不冷血嗜杀(但让属下去做)或不伤害儿童(如果可能的话)。他们认为这些良心上的原则使自己比一般不合人道的恶人水准高。诡计多端扩展自己势力并他的压迫人民的贵族是一个守序邪恶的例子。某些守序邪恶的人或生物狂热的效忠于邪恶，就好像十字军效忠于良善一样。伤害别人是他们这么做的目的，传播邪恶本身也是他们乐于如此的原因。他们也可能认为行恶是对某种邪恶神明或主人的责任的一部分。守序邪恶有时被称为“恶魔般的”，因为恶魔是守序邪恶的化身和典型。守序邪恶是一个有方法有意图并且能常常有所成就的邪恶阵营。"
    },
    ne: {
      name: "中立邪恶",
      english: "Neutral Evil",
      description: "中立邪恶的人物为了自己可以做出任何事，一切都是为了自己，就这么简单。他们从不为死在手下的人掉泪，不论是为财、为了高兴或只是为了方便。他们不喜欢纪律，也不遵守法律、传统或任何高贵的信念。然而，他们也不像混乱邪恶者那样浮躁不安，或热爱冲突。有些中立邪恶者将邪恶视为一种理想，想要献身于邪恶。这种恶人大多是邪恶神祇或秘密组织的成员。一般人习惯将中立邪恶称为“真正的邪恶”。中立邪恶的可怕在于表现出全然的邪恶，完全没有荣誉感和对象区别。"
    },
    ce: {
      name: "混乱邪恶",
      english: "Chaotic Evil",
      description: "混乱邪恶的人物会因为贪婪、憎恨或欲望而做出任何事。他暴躁易怒、满怀恶意、独断暴力而且无法预料。为了得到想要的东西，他会冲动而鲁莽地行动，散播邪恶与混乱。所幸他的计划大多杂乱无章，其团体大多组织散乱。一般而言，混乱邪恶者只有被强迫时才会与人合作，其领袖常要面对斗争与暗杀。混乱邪恶的可怕在于不仅破坏美丽与生命，也破坏了美丽与生命赖以存在的秩序。"
    }
  };

  const GRID_ORDER = ["lg", "ng", "cg", "ln", "nn", "cn", "le", "ne", "ce"];
  const TOTAL_QUESTIONS = SECTIONS.reduce(function (sum, section) {
    return sum + section.questions.length;
  }, 0);

  function createElement(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (typeof text === "string") node.textContent = text;
    return node;
  }

  function renderQuestions(root) {
    let number = 0;
    const fragment = document.createDocumentFragment();

    SECTIONS.forEach(function (section) {
      const sectionNode = createElement("section", "dnd-alignment-section");
      sectionNode.appendChild(createElement("h2", "", section.title));

      section.questions.forEach(function (question) {
        number += 1;
        const fieldset = createElement("fieldset", "dnd-alignment-question");
        fieldset.dataset.question = String(number);
        fieldset.appendChild(createElement("legend", "", String(number) + ". " + question[0]));

        const options = createElement("div", "dnd-alignment-options");
        question[1].forEach(function (option, optionIndex) {
          const label = createElement("label", "dnd-alignment-option");
          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = "dnd-alignment-q" + number;
          radio.value = String(optionIndex);
          radio.dataset.influence = option[1];
          radio.dataset.score = String(option[2]);
          radio.setAttribute("aria-label", String.fromCharCode(65 + optionIndex) + "：" + option[0]);

          const optionText = createElement(
            "span",
            "",
            String.fromCharCode(65 + optionIndex) + "．" + option[0]
          );
          label.appendChild(radio);
          label.appendChild(optionText);
          options.appendChild(label);
        });

        fieldset.appendChild(options);
        sectionNode.appendChild(fieldset);
      });

      fragment.appendChild(sectionNode);
    });

    root.appendChild(fragment);
  }

  function selectedInputs(form) {
    return Array.from(form.querySelectorAll('input[type="radio"]:checked'));
  }

  function updateProgress(app, form) {
    const completed = selectedInputs(form).length;
    const percent = Math.round((completed / TOTAL_QUESTIONS) * 100);
    const text = app.querySelector("#dnd-alignment-progress-text");
    const bar = app.querySelector("#dnd-alignment-progress-bar");
    const track = app.querySelector(".dnd-alignment-progress-track");

    if (text) text.textContent = "已完成 " + completed + " / " + TOTAL_QUESTIONS;
    if (bar) bar.style.width = percent + "%";
    if (track) track.setAttribute("aria-valuenow", String(completed));
  }

  function scoreAnswers(inputs) {
    const totals = { lx: 0, nx: 0, cx: 0, xg: 0, xn: 0, xe: 0 };
    inputs.forEach(function (input) {
      const key = input.dataset.influence;
      if (Object.prototype.hasOwnProperty.call(totals, key)) {
        totals[key] += Number(input.dataset.score || 0);
      }
    });
    return totals;
  }

  function dominantAxis(first, neutral, last) {
    const max = Math.max(first.value, neutral.value, last.value);
    const winners = [first, neutral, last].filter(function (item) {
      return item.value === max;
    });
    return winners.length === 1 ? winners[0].code : neutral.code;
  }

  function alignmentScores(totals) {
    return {
      lg: totals.lx + totals.xg,
      ng: totals.nx + totals.xg,
      cg: totals.cx + totals.xg,
      ln: totals.lx + totals.xn,
      nn: totals.nx + totals.xn,
      cn: totals.cx + totals.xn,
      le: totals.lx + totals.xe,
      ne: totals.nx + totals.xe,
      ce: totals.cx + totals.xe
    };
  }

  function determineAlignment(totals) {
    const order = dominantAxis(
      { code: "l", value: totals.lx },
      { code: "n", value: totals.nx },
      { code: "c", value: totals.cx }
    );
    const moral = dominantAxis(
      { code: "g", value: totals.xg },
      { code: "n", value: totals.xn },
      { code: "e", value: totals.xe }
    );
    return order + moral;
  }

  function renderAxis(container, rows) {
    container.replaceChildren();
    rows.forEach(function (row) {
      const line = createElement("div", "dnd-alignment-axis-row");
      line.appendChild(createElement("span", "", row.name));

      const track = createElement("div", "dnd-alignment-axis-bar");
      const fill = document.createElement("span");
      fill.style.width = Math.min(100, (row.value / 36) * 100) + "%";
      track.appendChild(fill);
      line.appendChild(track);
      line.appendChild(createElement("strong", "", String(row.value)));
      container.appendChild(line);
    });
  }

  function buildReportText(respondent, code, totals, scores) {
    const alignment = ALIGNMENTS[code];
    const lines = [
      (respondent ? respondent + "的" : "") + "D&D 阵营测试结果：" + alignment.name + "（" + alignment.english + "）",
      "秩序轴：守序 " + totals.lx + " / 中立 " + totals.nx + " / 混乱 " + totals.cx,
      "道德轴：善良 " + totals.xg + " / 中立 " + totals.xn + " / 邪恶 " + totals.xe,
      "九阵营得分：" + GRID_ORDER.map(function (itemCode) {
        return ALIGNMENTS[itemCode].name + " " + scores[itemCode];
      }).join("、"),
      "结果说明：" + alignment.description,
      window.location.href
    ];
    return lines.join("\n");
  }

  function renderResult(app, totals, respondent) {
    const code = determineAlignment(totals);
    const alignment = ALIGNMENTS[code];
    const scores = alignmentScores(totals);
    const result = app.querySelector("#dnd-alignment-result");

    app.querySelector("#dnd-alignment-result-title").textContent =
      alignment.name + "（" + alignment.english + "）";
    app.querySelector("#dnd-alignment-result-subtitle").textContent =
      respondent ? "作答者：" + respondent : "未填写作答者或角色名";
    app.querySelector("#dnd-alignment-result-description").textContent = alignment.description;

    renderAxis(app.querySelector("#dnd-alignment-order-scores"), [
      { name: "守序", value: totals.lx },
      { name: "中立", value: totals.nx },
      { name: "混乱", value: totals.cx }
    ]);
    renderAxis(app.querySelector("#dnd-alignment-moral-scores"), [
      { name: "善良", value: totals.xg },
      { name: "中立", value: totals.xn },
      { name: "邪恶", value: totals.xe }
    ]);

    const grid = app.querySelector("#dnd-alignment-grid");
    grid.replaceChildren();
    GRID_ORDER.forEach(function (itemCode) {
      const cell = createElement(
        "div",
        "dnd-alignment-cell" + (itemCode === code ? " is-result" : "")
      );
      cell.appendChild(createElement("strong", "", ALIGNMENTS[itemCode].name));
      cell.appendChild(createElement("span", "", ALIGNMENTS[itemCode].english + " · " + scores[itemCode] + " 分"));
      grid.appendChild(cell);
    });

    const copy = app.querySelector("#dnd-alignment-copy");
    copy.dataset.report = buildReportText(respondent, code, totals, scores);
    result.hidden = false;
    result.focus({ preventScroll: true });
    result.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function copyReport(button) {
    const report = button.dataset.report || "";
    if (!report) return;

    try {
      await navigator.clipboard.writeText(report);
    } catch (_) {
      const textarea = document.createElement("textarea");
      textarea.value = report;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      textarea.remove();
    }

    const original = button.dataset.originalText || button.textContent;
    button.dataset.originalText = original;
    button.textContent = "已复制";
    window.setTimeout(function () {
      button.textContent = original;
    }, 1600);
  }

  function resetTest(app, form) {
    form.reset();
    app.querySelectorAll(".dnd-alignment-question").forEach(function (fieldset) {
      fieldset.classList.remove("is-missing");
    });
    const error = app.querySelector("#dnd-alignment-error");
    error.hidden = true;
    error.textContent = "";
    const result = app.querySelector("#dnd-alignment-result");
    result.hidden = true;
    app.querySelector("#dnd-alignment-respondent").value = "";
    updateProgress(app, form);
    app.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function init() {
    const app = document.getElementById("dnd-alignment-app");
    if (!app || app.dataset.initialized === "1") return;
    app.dataset.initialized = "1";

    const form = app.querySelector("#dnd-alignment-form");
    const questionsRoot = app.querySelector("#dnd-alignment-questions");
    renderQuestions(questionsRoot);
    updateProgress(app, form);

    form.addEventListener("change", function (event) {
      if (!event.target.matches('input[type="radio"]')) return;
      const fieldset = event.target.closest(".dnd-alignment-question");
      if (fieldset) fieldset.classList.remove("is-missing");
      updateProgress(app, form);
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const inputs = selectedInputs(form);
      const missing = Array.from(app.querySelectorAll(".dnd-alignment-question")).filter(function (fieldset) {
        return !fieldset.querySelector('input[type="radio"]:checked');
      });
      const error = app.querySelector("#dnd-alignment-error");

      app.querySelectorAll(".dnd-alignment-question").forEach(function (fieldset) {
        fieldset.classList.remove("is-missing");
      });

      if (missing.length > 0) {
        missing.forEach(function (fieldset) {
          fieldset.classList.add("is-missing");
        });
        error.textContent = "还有 " + missing.length + " 题未作答，请完成标红的题目后再生成报告。";
        error.hidden = false;
        missing[0].scrollIntoView({ behavior: "smooth", block: "center" });
        const firstRadio = missing[0].querySelector('input[type="radio"]');
        if (firstRadio) firstRadio.focus({ preventScroll: true });
        return;
      }

      error.hidden = true;
      const respondent = app.querySelector("#dnd-alignment-respondent").value.trim();
      renderResult(app, scoreAnswers(inputs), respondent);
    });

    app.querySelector("#dnd-alignment-reset").addEventListener("click", function () {
      resetTest(app, form);
    });
    app.querySelector("#dnd-alignment-copy").addEventListener("click", function (event) {
      copyReport(event.currentTarget);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  if (typeof window !== "undefined" && window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(function () {
      window.setTimeout(init, 0);
    });
  }
})();
