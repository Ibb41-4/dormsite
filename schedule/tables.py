import django_tables2 as tables


class WeeksTable(tables.Table):
    week = tables.DateColumn(verbose_name="Week", accessor="Week")
    keukenbeurt1 = tables.Column(verbose_name="Keukenbeurt", accessor="Keukenbeurt 1")
    shift1_done = tables.CheckBoxColumn(verbose_name="Keukenbeurt", accessor="Keukenbeurt 1_done")
    keukenbeurt2 = tables.Column(verbose_name="Keukenbeurt", accessor="Keukenbeurt 2")
    shift2_done = tables.CheckBoxColumn(verbose_name="Keukenbeurt", accessor="Keukenbeurt 2_done")
    kortegang = tables.Column(verbose_name="Korte gang", accessor="Korte gang")
    shift3_done = tables.CheckBoxColumn(verbose_name="Keukenbeurt", accessor="Korte gang_done")
    langegang = tables.Column(verbose_name="Lange gang", accessor="Lange gang")
    shift4_done = tables.CheckBoxColumn(verbose_name="Keukenbeurt", accessor="Lange gang_done")

    '''class Meta:
        model = Week
        exclude = ('id', 'number', 'year', )
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        #sequence = ("startdate", "id", "task1")'''
