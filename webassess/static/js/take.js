$.extend(true, quest, {
    map: {
    // qid: aid
    },
    curqid: 0,
    curqnum: 0,
    status: "",
    goback: function() {
        if(this.status == "review") return this.unreview();
        if(this.curqnum <= 1) return;
        this.nexttext();
        this.curqnum--;
        this.display(this.questions[this.curqnum-1].id);
    },
    getqid: function(qid) {
        return this.questions.filter(function(t){return t.id == qid;})[0];
    },
    getaid: function(q, aid) {
        return q.choices.filter(function(t){return t.id == aid;})[0];
    },
    gonext: function() { console.log('n '+this.curqnum);
        if(this.status == "review") return this.submittest();
        if(this.curqnum >= this.numqs) return this.review();
        this.nexttext();
        this.curqnum++;
        this.display(this.questions[this.curqnum-1].id);
    },
    submittest: function() {
        this.clearls();
        $.post('/quest/submit/', data = {
            'testid': this.TESTID,
            'map': JSON.stringify(this.map),
            'questions': JSON.stringify(this.questions)
        }, function(d) {
            location.href = '/dashboard/?complete='+this.TESTID
        });
        console.log('Sending',data);
    },
    nexttext: function() {
        if(this.curqnum == this.numqs - 1) $("button.gon").html("Review Test");
        else $("button.gon").html("Next");
    },
    display: function(qid) {
        this.curqid = qid;
        var q = this.getqid(qid);
        $(".cq-html").html(q.html);
        $(".cq-curqnum").html(this.curqnum);
        $("input.qnum").attr("value", this.curqnum);
        console.log(q);
        $(".cq-choices").html("");
        var opt = 0;
        for(var i=0 in j=q.choices) {
            console.log(j[i]);
            $(".cq-choices").append(
                "<div class='qc-opt opt"+(++opt)+"'>" +
                "<input name='qchoice' class='qchoice' type='radio' value="+opt+" />" +
                "<span class='qc-opttext'>"+j[i].html+"</span>" +
                "</div>"
            );
            this.mapevents();
            if(typeof this.map[qid] != 'undefined') $('input.qchoice[value='+this.map[qid]+']').attr('checked',true);
        }

    },
    jump: function(qid) {
        var n = 0;
        for(var i in j=this.questions) {
            if(this.questions[n] == j[i]) break;
            n++;
        }
        this.curqnum = n;
        this.display(qid);
    },
    review: function() {
        this.status = "review";
        this.curqnum--;
        $("button.gon").html("Submit Test");
        $("button.gop").html("Back to Test");
        $(".qcontents .review").show();
        $(".qcontents .qhtml, .qcontents .qoptions").hide();
        $(".review table").html("");
        for(var i in j=this.map) {
        /*    console.log('i'+i);
            var q = window.q= this.getqid(i), ai = 0;
            var a = window.a= quest.getaid(q, parseInt(this.map[i]));
            $(".review table").append(
                "<tr data-id='"+i+"'>" +
                "<td>#"+i+"</td><td>"+q.html.replace(/<(.|\n)*?>/, '')+"</td>" +
                "<td>You said <span title=\""+j[i]+"\">"+a.html.replace(/<(.|\n)*?>/, '')+"</span></td>" +
                "</tr>");*/
            var q = this.getqid(i);
            var a = q.choices[this.map[i]-1];
            
            $(".review table").append(
                "<tr data-id='"+i+"'>" +
                "<td>#"+i+"</td><td>"+q.html.replace(/<(.|\n)*?>/, '')+"</td>" +
                "<td>You said <span title=\""+a.id+"\">"+a.html.replace(/<(.|\n)*?>/, '')+"</span></td>" +
                "</tr>");
        }
        $(".review table > tr").click(function() {
            this.jump($(this).attr('data-id'));
        })
    },
    unreview: function() {
        this.status = "";
        $("button.gon").html("Next");
        $("button.gop").html("Previous");
        console.log('a'+this.curqid);
        //qd = this.curqnum;
        this.curqnum++;
        this.display(this.curqid);

        console.log('a'+this.curqid);
        $(".qcontents .review").hide();
        $(".qcontents .qhtml, .qcontents .qoptions").show();
        
    },
    init: function() {
        if(this.questions.length < 1) {
            $(".qcontents").html("<div style='font-size: 20px'>An error occurred loading this test.</div><p>There were no questions found in this test.</p>");
            throw 'questions.length='+this.questions.length;
            return;
        }
        this.loadls();
        $(".qnum-total").html(this.numqs);
        this.gonext();
    },
    loadls: function() {
        try {
            if(typeof localStorage[this.TESTID+'map'] != 'undefined') this.map = JSON.parse(localStorage[this.TESTID+'map']);
        } catch(e) { console.error('An error occurred reading from localStorage', e); }
    },
    clearls: function() {
        localStorage[this.TESTID+'map'] = null;
        localStorage.removeItem(this.TESTID+'map');
    },
    save: function(n) {
        this.map[this.curqid] = n;
        localStorage[this.TESTID+'map'] = JSON.stringify(this.map);
        console.log('map:',this.map);
    },
    mapevents: function() {
        $("input.qchoice").change(function() { quest.save($(this).val()); })
    }

});