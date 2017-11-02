var fsm = new StateMachine({
    init: 'playerTurn',
    transitions: [
        { name: 'playerMove', from: 'playerTurn', to: 'computerTurn' },
        { name: 'computerMove', from: 'computerTurn', to: 'playerTurn' },
    ],

    data: {
        board: 4,
    },

    methods: {
        onPlayerMove: function(lifecycle, amount) {
            this.board -= amount;
            $("#board span").text(this.board);
        },
        onComputerMove: function() {
            self = this;
            return $.ajax({
                type: "GET",
                url: "http://127.0.0.1:8000/",
                dataType: 'json',
                data: {pos: self.board },
            }).done(function (resp) {
                self.board -= resp;
                $("#board span").text(self.board);
            });
        },
    },
});

window.setInterval(function() {
    fsm.computerMove();
}, 2000);

function play(amount) {
    fsm.playerMove(amount);
}
