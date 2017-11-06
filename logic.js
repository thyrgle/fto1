/**
 * A representation of the game four to one that 
 */
var game = new StateMachine({
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

$('document').ready(function() {
    /**
     * Remove one "stone" from the board.
     */
    $("#remove1").on('click', function() {
        game.playerMove(1);
    });

    /**
     * Remove two "stones" from the board.
     */
    $("#remove2").click(function() {
        game.playerMove(2);
    });

    /**
     * Check for updates in the state, used to determine if the computer can m-
     * ake a move.
     */
    window.setInterval(function() {
        game.computerMove();
    }, 2000);
});
