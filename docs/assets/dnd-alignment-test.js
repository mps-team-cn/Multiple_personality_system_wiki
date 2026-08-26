/*
 * D&D 九宫格阵营测试
 * - 纯前端计算，不存储、不发送答案
 * - 测试题与计分据经典 D&D 3e《Hero Builder's Guidebook》36 题阵营测试
 * - 中文题目据 PA D&D Alignment Test 英文原文翻译
 * - 阵营释义参考 D&D 2024（5R）
 * - 仅在包含 #dnd-alignment-app 的页面激活
 */
(function () {
  "use strict";

  const SECTIONS = [
    {
      title: "第一部分：家族",
      questions: [
        ["家族长辈正在向其他家族成员表达对你的不满。你会：", [
          ["接受批评，并改变自己的做法", "xg", 2],
          ["设法与他们达成妥协", "xg", 1],
          ["无视他们的轻蔑，同时败坏这些长辈的名声", "xe", 1],
          ["不惜一切办法让他们闭嘴", "xe", 2]
        ]],
        ["家族急需帮助时，你会放弃一份前途光明的事业吗？", [
          ["会，毫不犹豫", "xg", 2],
          ["会，但会有些不情愿", "xg", 1],
          ["只有在确定自己很快能重返事业时才会", "xn", 1],
          ["不会", "xn", 2]
        ]],
        ["你会为了推进自己的事业而背叛一位家族成员吗？", [
          ["会，丝毫不会感到内疚", "xe", 2],
          ["会，只要能暗中进行", "xe", 1],
          ["我会抵抗这种诱惑", "xn", 1],
          ["我觉得这种想法令人厌恶", "xn", 2]
        ]],
        ["你尊重家族领袖吗？", [
          ["他们的话指引着我的行动", "lx", 2],
          ["他们是我的榜样", "lx", 1],
          ["他们往往不了解我的生活", "cx", 1],
          ["他们根本不了解现实", "cx", 2]
        ]],
        ["如果家族安排你与一个令你厌恶的人结婚，你会：", [
          ["接受婚事，并为能效力家族而自豪", "lx", 2],
          ["答应婚事，但掩饰自己的不情愿", "lx", 1],
          ["暗中设法阻挠这桩婚事", "nx", 1],
          ["逃走", "nx", 2]
        ]],
        ["你与一位家族成员关系疏远。对方临终前希望与你和解。你会：", [
          ["与对方交谈，但坚持自己的立场", "cx", 1],
          ["拒绝与对方交谈", "cx", 2],
          ["坦率而不带怨恨地谈论你们疏远的原因", "nx", 1],
          ["主动寻求和解，并听取对方的临终遗言", "nx", 2]
        ]]
      ]
    },
    {
      title: "第二部分：朋友",
      questions: [
        ["一位权势显赫却腐败的法官以财富为条件，要你出庭指证朋友。你会：", [
          ["指证朋友并收下钱", "xe", 2],
          ["收钱作证，但尽量让自己的证词不起作用", "xe", 1],
          ["拒绝这项提议，也拒绝出庭作证", "xg", 1],
          ["不计后果地出庭为朋友作证", "xg", 2]
        ]],
        ["你容易与朋友建立亲密关系，还是倾向于和大多数人保持距离？", [
          ["我有许多亲密朋友", "xg", 2],
          ["我有一些亲密朋友", "xg", 1],
          ["我只有少数亲密朋友", "xn", 1],
          ["我尽量与人保持距离", "xn", 2]
        ]],
        ["你背叛过朋友吗？", [
          ["不止一次，而且有时我没有受到惩罚", "xe", 2],
          ["有过一次", "xe", 1],
          ["我曾动过念头，但从未真的做过", "xn", 1],
          ["我绝不会考虑这种事", "xn", 2]
        ]],
        ["你如何看待与一位伴侣相守终生的承诺？", [
          ["我拥有或希望拥有这样的爱情", "lx", 2],
          ["这样的爱情很理想——如果真能实现的话", "lx", 1],
          ["我担心这样会错过与其他人发展关系的可能性", "cx", 1],
          ["把自己绑在一个人身上？大错特错", "cx", 2]
        ]],
        ["借钱给朋友时，你会坚持要求对方偿还吗？", [
          ["会，而且我会写好契约，以免产生误会", "lx", 2],
          ["会，但我会尽量在具体条件上保持灵活", "lx", 1],
          ["不会，不过对方愿意还钱当然很好", "nx", 1],
          ["不会，这样他们就欠我一个人情", "nx", 2]
        ]],
        ["你仍与儿时玩伴保持联络吗？", [
          ["是的，我们定期通信", "nx", 2],
          ["是的，我们努力保持联络", "nx", 1],
          ["没有，我太常搬家了", "cx", 1],
          ["没有，我和他们已经没有共同之处", "cx", 2]
        ]]
      ]
    },
    {
      title: "第三部分：集体与归属",
      questions: [
        ["你会投入时间和金钱来改善自己所属的集体吗？", [
          ["会，集体的需要是我的首要考虑", "xg", 2],
          ["会，在满足自己的需要后，我会尽可能多地捐助", "xg", 1],
          ["不会，我没有多余的时间或金钱", "xn", 1],
          ["不会，把时间和金钱花在所属集体上纯属浪费", "xn", 2]
        ]],
        ["你所属的集体面临严重的外部威胁，甚至可能因此覆灭。你会：", [
          ["战斗至最后一息，保卫集体", "xg", 2],
          ["与集体中的其他人一同保卫大家", "xg", 1],
          ["局势一变得严峻就逃走", "xe", 1],
          ["与敌人达成交易，充当间谍", "xe", 2]
        ]],
        ["如果你受伤并需要立即帮助，集体中的其他人会愿意帮助你吗？", [
          ["会，因为他们知道我也会这样帮助他们", "xn", 2],
          ["会，因为我在集体中通常很受欢迎", "xn", 1],
          ["可能不会，因为集体中的人不信任我", "xe", 1],
          ["肯定不会，我在集体中树过一些敌人", "xe", 2]
        ]],
        ["你尊重所属集体的规则和管理者吗？", [
          ["是的，毫无疑问", "lx", 2],
          ["是的，总体而言，这是最好的治理方式", "lx", 1],
          ["看情况——有些规则我就是不认同", "cx", 1],
          ["我不理会那些管理者；他们管不到我", "cx", 2]
        ]],
        ["集体中的其他人会排斥、躲避或嘲笑你吗？", [
          ["会，他们狭隘的头脑容不下不符合常规的人", "cx", 2],
          ["有些人会，因为我并非总能融入集体", "cx", 1],
          ["不会，大家通常认为我很正常", "nx", 1],
          ["不会，我就是集体里衡量‘正常’的标准", "nx", 2]
        ]],
        ["你会担任管理或代表性的职责，为集体成员的利益发声吗？", [
          ["我会欣然接受这份荣誉", "lx", 2],
          ["当然，这是每个人的责任", "lx", 1],
          ["只有在没有其他人能胜任时才会", "nx", 1],
          ["不会，我不想为集体的福祉负责", "nx", 2]
        ]]
      ]
    },
    {
      title: "第四部分：国家",
      questions: [
        ["你的国家正遭受饥荒。你会：", [
          ["把自己拥有的食物与他人分享", "xg", 2],
          ["自己尽量少吃，把剩下的分给他人", "xg", 1],
          ["偷取维持生存所需的食物", "xe", 1],
          ["尽可能多地偷取食物，再高价卖回给社区", "xe", 2]
        ]],
        ["如果报酬足够高，你会在国王的酒杯中下毒吗？", [
          ["会，我以前做过类似的事", "xe", 2],
          ["会，只要我认为自己能逃脱惩罚", "xe", 1],
          ["不会，尽管巨额报酬会让我心动", "xn", 1],
          ["不会，而且我会警告国王有人图谋下毒", "xn", 2]
        ]],
        ["一场瘟疫正在席卷你的国家。你会：", [
          ["承担寻找解药的危险任务", "xg", 2],
          ["尽己所能医治病人", "xg", 1],
          ["避免接触病人", "xn", 1],
          ["逃离国家", "xn", 2]
        ]],
        ["你尊重这片土地上统治者的合法权威吗？", [
          ["尊重，女王万岁！", "lx", 2],
          ["是的，我们的统治者大体上公平、公正", "lx", 1],
          ["不尊重，统治者并不比任何人高一等", "cx", 1],
          ["不尊重，统治者无一例外都会被权力腐化", "cx", 2]
        ]],
        ["如果有人开出一笔相当丰厚的报酬，你会为敌对的外国势力充当间谍吗？", [
          ["会，因为这个国家也该受点挫折", "cx", 2],
          ["会，因为国家机密对我来说无关紧要", "cx", 1],
          ["不会，因为我可能会被抓", "nx", 1],
          ["不会，因为我绝不会辜负国家对我的信任", "nx", 2]
        ]],
        ["你依靠政府来执行契约并保障财产权吗？", [
          ["是的，因为维护法治比任何个人纠纷都重要", "lx", 2],
          ["是的，因为法院最适合处理这类纠纷", "lx", 1],
          ["你在开玩笑吗？政府连路都铺不好", "nx", 1],
          ["绝不。如果我不能亲自守住财产，就不配拥有它", "nx", 2]
        ]]
      ]
    },
    {
      title: "第五部分：法律与刑罚",
      questions: [
        ["如果你被监禁，你会为了逃脱而伤害或杀死他人吗？", [
          ["会。谁让他们把我关起来，活该", "xe", 2],
          ["会。他们干这份工作时就知道有这种风险", "xe", 1],
          ["不会，除非只是造成很快能痊愈的轻伤", "xn", 1],
          ["不会。那些守卫只是在履行职责", "xn", 2]
        ]],
        ["你认同贵族有权恶劣对待在其土地上劳作的农奴吗？", [
          ["认同。他们该庆幸自己不是奴隶", "xn", 2],
          ["认同，因为有时只有恐惧能促使他们干活", "xn", 1],
          ["不认同，贵族应当尽可能仁慈地统治", "xg", 1],
          ["不认同。任何人都没有‘权利’恶劣对待别人，绝无例外", "xg", 2]
        ]],
        ["你无意中犯了罪。你会：", [
          ["投案自首，并设法补偿受害者", "xg", 2],
          ["投案自首，请求法庭宽大处理", "xg", 1],
          ["隐瞒自己牵涉其中的事实，必要时说谎", "xe", 1],
          ["设法把罪名栽赃给别人", "xe", 2]
        ]],
        ["如果确实犯了罪，你会认罪吗？", [
          ["会，因为认罪是我的责任", "lx", 2],
          ["会，因为这样或许能获得较轻的判决", "lx", 1],
          ["不会，我会让司法官证明我有罪", "nx", 1],
          ["不会，而且我会设法‘证明’自己无罪", "nx", 2]
        ]],
        ["如果表达具有革命色彩的政治观点会受到惩罚，你还会公开表达吗？", [
          ["会，我宁愿受罚也不愿保持沉默", "cx", 2],
          ["会，总要有人说真话", "cx", 1],
          ["不会，尽管私下会对朋友说", "nx", 1],
          ["不会，政治不值得我为此惹上麻烦", "nx", 2]
        ]],
        ["旅行途中，你目击了一场袭击。你被要求出庭作证，这将严重耽误行程。你会：", [
          ["夜里溜出城镇，逃避作证", "cx", 2],
          ["说自己什么也没看到", "cx", 1],
          ["不情愿地留下，作完证后便离开", "lx", 1],
          ["一直留到审判结束，以备需要进一步作证", "lx", 2]
        ]]
      ]
    },
    {
      title: "第六部分：财富与工作",
      questions: [
        ["财富的最佳用途是什么？", [
          ["帮助穷人和不幸的人", "xg", 2],
          ["满足亲友的需要", "xg", 1],
          ["让自己稳居顶层", "xe", 1],
          ["不仅让自己稳居顶层，还要阻止别人爬到同一高度", "xe", 2]
        ]],
        ["遇到乞丐，你会：", [
          ["慷慨施舍", "xg", 2],
          ["适量施舍", "xg", 1],
          ["只给即使失去也不心疼的钱——最多一两块钱", "xn", 1],
          ["从旁走过，视而不见", "xn", 1]
        ]],
        ["通过魔法，你可以使村里的商人以为你的铜币是金币。你会这样做吗？", [
          ["会，而且会尽可能多买东西", "xe", 2],
          ["会，但只骗富商", "xe", 1],
          ["不会，风险太大", "xn", 1],
          ["不会，商人也要养家糊口", "xn", 2]
        ]],
        ["你收到两份工作邀请：一份薪酬更高，另一份安稳可靠。你会选哪一份？", [
          ["肯定选高薪的；安稳工作听起来实在太乏味了", "nx", 2],
          ["大概选高薪的，不过我也会了解一下安稳的那份", "nx", 1],
          ["选安稳的，除非另一份工作的薪酬高得惊人", "lx", 1],
          ["肯定选安稳的，因为我会做长远规划", "lx", 2]
        ]],
        ["最佳的致富途径是什么？", [
          ["这关乎天时地利，还有一时运气", "cx", 2],
          ["灵活变通会带来更多机会", "cx", 1],
          ["按照一个包含自己能够接受的风险水平的长期计划来做", "lx", 1],
          ["努力工作，坚持不懈", "lx", 2]
        ]],
        ["如果你接受了一份工作或契约，后来任务变得危险得多，你还会努力完成吗？", [
          ["会，我一诺千金", "nx", 2],
          ["会，因为保持值得信赖的声誉很重要", "nx", 1],
          ["我肯定会要求重新协商条件", "cx", 1],
          ["如果这已经不是一笔划算的交易，约定就此作废", "cx", 2]
        ]]
      ]
    }
  ];

  const ALIGNMENTS = {
    lg: {
      name: "守序善良",
      english: "Lawful Good",
      description: "守序善良的人努力做正确的事，同时重视社会规范、责任与秩序。他们通常相信良好的制度、承诺和规则能够保护他人，并愿意在这些原则下帮助他人、维护正义。"
    },
    ng: {
      name: "中立善良",
      english: "Neutral Good",
      description: "中立善良的人会尽己所能去帮助他人、做正确的事。他们可以遵循规则和社会规范，但不会认为自己必须受到这些规则束缚；当规则妨碍善行时，他们更看重事情本身是否正确。"
    },
    cg: {
      name: "混乱善良",
      english: "Chaotic Good",
      description: "混乱善良的人依照自己的良知行事，很少因为社会期待、传统或权威而改变判断。他们珍视自由，也愿意帮助他人；如果规则与自己认定的正义发生冲突，他们通常会选择良知。"
    },
    ln: {
      name: "守序中立",
      english: "Lawful Neutral",
      description: "守序中立的人重视法律、传统、职责或个人信条，并倾向于按照明确的原则行动。对他们而言，可靠、一致和遵守准则本身十分重要，而善恶通常不是决定行动的首要因素。"
    },
    nn: {
      name: "绝对中立",
      english: "True Neutral",
      description: "绝对中立的人通常不愿在善恶或秩序与混乱之间明确站队。他们更倾向于根据具体情况判断，在当下选择自己认为最合理、最合适的做法，而不是坚持某一种阵营理念。"
    },
    cn: {
      name: "混乱中立",
      english: "Chaotic Neutral",
      description: "混乱中立的人重视个人自由，倾向于按照自己的想法和当下判断行动，不喜欢受到规则、传统或他人期待的约束。他们并不必然希望帮助或伤害别人，只是不愿让外界替自己决定该怎么做。"
    },
    le: {
      name: "守序邪恶",
      english: "Lawful Evil",
      description: "守序邪恶的人会有计划地追求自己的利益，即使因此伤害他人。他们仍然重视某种秩序，例如法律、传统、忠诚关系或个人准则，并倾向于在这些限制范围内取得自己想要的东西。"
    },
    ne: {
      name: "中立邪恶",
      english: "Neutral Evil",
      description: "中立邪恶的人首先考虑自己的利益，只要认为值得且能够承担后果，就可能利用或伤害他人。他们既不会因为秩序而约束自己，也不会为了反抗秩序而行动，核心通常只是怎样最有利于自己。"
    },
    ce: {
      name: "混乱邪恶",
      english: "Chaotic Evil",
      description: "混乱邪恶的人受贪欲、仇恨、欲望或冲动驱使，可能任意伤害他人，并且很少在意法律、传统或他人的权利。他们既缺少对他人的善意，也厌恶外界约束，是九种阵营中最倾向于破坏与暴力的一类。"
    }
  };

  const GRID_ORDER = ["lg", "ng", "cg", "ln", "nn", "cn", "le", "ne", "ce"];
  const RESULT_NOTE = "分数只反映这轮答案在本测试规则下的相对倾向。只有最高分精确同分时才标记边界；分数接近但不同不会改变 canonical 九宫格结果。";
  const AXIS_NAMES = {
    order: { l: "守序", n: "中立", c: "混乱" },
    moral: { g: "善良", n: "中立", e: "邪恶" }
  };
  const TOTAL_QUESTIONS = SECTIONS.reduce(function (sum, section) {
    return sum + section.questions.length;
  }, 0);
  const AXIS_MAXIMUMS = calculateAxisMaximums();

  function calculateAxisMaximums() {
    const maximums = { lx: 0, nx: 0, cx: 0, xg: 0, xn: 0, xe: 0 };

    SECTIONS.forEach(function (section) {
      section.questions.forEach(function (question) {
        const questionMaximums = {};
        question[1].forEach(function (option) {
          const key = option[1];
          const score = Number(option[2] || 0);
          if (Object.prototype.hasOwnProperty.call(maximums, key)) {
            questionMaximums[key] = Math.max(questionMaximums[key] || 0, score);
          }
        });
        Object.keys(questionMaximums).forEach(function (key) {
          maximums[key] += questionMaximums[key];
        });
      });
    });

    return maximums;
  }

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
    let state = "dominant";
    if (winners.length === 3) {
      state = "full_tie";
    } else if (winners.length === 2) {
      state = winners.some(function (item) { return item.code === neutral.code; })
        ? "boundary"
        : "extreme_tie";
    }

    return {
      code: winners.length === 1 ? winners[0].code : neutral.code,
      state: state,
      winners: winners.map(function (item) { return item.code; })
    };
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

  function determineAlignmentDetails(totals) {
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
    const candidates = [];
    order.winners.forEach(function (orderCode) {
      moral.winners.forEach(function (moralCode) {
        candidates.push(orderCode + moralCode);
      });
    });
    return {
      code: order.code + moral.code,
      order: order,
      moral: moral,
      candidates: candidates
    };
  }

  function determineAlignment(totals) {
    return determineAlignmentDetails(totals).code;
  }

  function axisStateText(axisName, axisResult) {
    const names = AXIS_NAMES[axisName];
    const winnerNames = axisResult.winners.map(function (code) { return names[code]; });
    const label = axisName === "order" ? "秩序轴" : "道德轴";

    if (axisResult.state === "boundary") {
      return label + "边界：" + winnerNames.join(" ↔ ") + "。";
    }
    if (axisResult.state === "extreme_tie") {
      return label + "特殊平局：" + winnerNames.join(" ↔ ") + "；两端同分且中立更低，这不同于通常意义上的中立。";
    }
    if (axisResult.state === "full_tie") {
      return label + "无明显单一倾向：" + winnerNames.join(" / ") + "完全同分。";
    }
    return "";
  }

  function boundarySummary(determination) {
    const ambiguousAxes = [determination.order, determination.moral].filter(function (axis) {
      return axis.state !== "dominant";
    });
    if (ambiguousAxes.length === 0) return [];

    const lines = [];
    if (ambiguousAxes.length === 2) {
      lines.push("双轴边界：");
    } else if (determination.order.state === "dominant") {
      lines.push("秩序倾向明确：" + AXIS_NAMES.order[determination.order.code] + "。");
    } else if (determination.moral.state === "dominant") {
      lines.push("道德倾向明确：" + AXIS_NAMES.moral[determination.moral.code] + "。");
    }

    [
      { name: "order", result: determination.order },
      { name: "moral", result: determination.moral }
    ].forEach(function (axis) {
      const text = axisStateText(axis.name, axis.result);
      if (text) lines.push(text);
    });

    const candidateNames = determination.candidates.map(function (code) {
      return ALIGNMENTS[code].name;
    });
    const hasExtremeTie = ambiguousAxes.some(function (axis) {
      return axis.state === "extreme_tie";
    });
    const hasFullTie = ambiguousAxes.some(function (axis) {
      return axis.state === "full_tie";
    });
    let candidateLabel = "可能的相邻阵营";
    if (hasExtremeTie && determination.candidates.length === 2) {
      candidateLabel = "特殊倾向";
    } else if (hasFullTie) {
      candidateLabel = "可能阵营";
    } else if (determination.candidates.length === 2) {
      candidateLabel = "边界倾向";
    }
    const candidateSeparator = candidateNames.length === 2 ? " ↔ " : " / ";
    lines.push(candidateLabel + "：" + candidateNames.join(candidateSeparator) + "。");

    if (determination.order.state === "full_tie" && determination.moral.state === "full_tie") {
      lines.push("本次测试没有形成明显的阵营倾向。两个轴均完全同分，因此“绝对中立”只是九宫格兼容结果，并不表示角色明确具有绝对中立倾向。");
    } else if (hasExtremeTie) {
      lines.push("canonical 九宫格结果按中立轴向兼容处理，但不能据此解释为普通中立倾向。");
    }
    return lines;
  }

  function renderAxis(container, rows) {
    container.replaceChildren();
    rows.forEach(function (row) {
      const maximum = AXIS_MAXIMUMS[row.key] || 1;
      const line = createElement("div", "dnd-alignment-axis-row");
      line.appendChild(createElement("span", "", row.name));

      const track = createElement("div", "dnd-alignment-axis-bar");
      track.setAttribute("role", "progressbar");
      track.setAttribute("aria-label", row.name + "得分");
      track.setAttribute("aria-valuemin", "0");
      track.setAttribute("aria-valuemax", String(maximum));
      track.setAttribute("aria-valuenow", String(row.value));
      const fill = document.createElement("span");
      fill.style.width = Math.min(100, (row.value / maximum) * 100) + "%";
      track.appendChild(fill);
      line.appendChild(track);
      line.appendChild(createElement("strong", "", row.value + " / " + maximum));
      container.appendChild(line);
    });
  }

  function buildReportText(respondent, determination, totals, scores) {
    const code = determination.code;
    const alignment = ALIGNMENTS[code];
    const boundaryLines = boundarySummary(determination);
    const lines = [
      (respondent ? respondent + "的" : "") + "D&D 阵营测试结果：" + alignment.name + "（" + alignment.english + "）",
      "秩序轴：守序 " + totals.lx + " / 中立 " + totals.nx + " / 混乱 " + totals.cx,
      "道德轴：善良 " + totals.xg + " / 中立 " + totals.xn + " / 邪恶 " + totals.xe
    ];
    boundaryLines.forEach(function (line) {
      lines.push("边界说明：" + line);
    });
    lines.push(
      "九阵营得分：" + GRID_ORDER.map(function (itemCode) {
        return ALIGNMENTS[itemCode].name + " " + scores[itemCode];
      }).join("、"),
      "结果说明：" + alignment.description,
      window.location.href
    );
    return lines.join("\n");
  }

  function renderResult(app, totals, respondent) {
    const determination = determineAlignmentDetails(totals);
    const code = determination.code;
    const alignment = ALIGNMENTS[code];
    const scores = alignmentScores(totals);
    const boundaryLines = boundarySummary(determination);
    const result = app.querySelector("#dnd-alignment-result");

    app.querySelector("#dnd-alignment-result-title").textContent =
      alignment.name + "（" + alignment.english + "）";
    app.querySelector("#dnd-alignment-result-subtitle").textContent =
      (boundaryLines.length > 0 ? "九宫格兼容结果 · " : "") +
      (respondent ? "作答者：" + respondent : "未填写作答者或角色名");
    app.querySelector("#dnd-alignment-result-description").textContent = alignment.description;

    renderAxis(app.querySelector("#dnd-alignment-order-scores"), [
      { key: "lx", name: "守序", value: totals.lx },
      { key: "nx", name: "中立", value: totals.nx },
      { key: "cx", name: "混乱", value: totals.cx }
    ]);
    renderAxis(app.querySelector("#dnd-alignment-moral-scores"), [
      { key: "xg", name: "善良", value: totals.xg },
      { key: "xn", name: "中立", value: totals.xn },
      { key: "xe", name: "邪恶", value: totals.xe }
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

    const resultNote = app.querySelector(".dnd-alignment-result-note");
    resultNote.textContent = (boundaryLines.length > 0 ? boundaryLines.join(" ") + " " : "") + RESULT_NOTE;

    const copy = app.querySelector("#dnd-alignment-copy");
    copy.dataset.report = buildReportText(respondent, determination, totals, scores);
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

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      SECTIONS: SECTIONS,
      dominantAxis: dominantAxis,
      determineAlignmentDetails: determineAlignmentDetails,
      determineAlignment: determineAlignment,
      boundarySummary: boundarySummary
    };
  }

  if (typeof document === "undefined") return;

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
