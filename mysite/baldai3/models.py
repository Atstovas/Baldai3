from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse  # Papildome imports
import uuid
from PIL import Image
from django.utils.html import format_html


class SideDrill(models.Model):
    side = models.CharField(verbose_name="Gręžimo kraštinė", max_length=10)

    def __str__(self):
        return f"{self.side}"

    class Meta:
        verbose_name = 'Gręžimo pusė'
        verbose_name_plural = 'Gręžimo pusės'


class DrillSketch(models.Model):
    drill = models.CharField(verbose_name="Gręžimo eskizas", max_length=20)
    sketch = models.ImageField(verbose_name="Eskizas", upload_to="sketch", null=True, blank=True)
    drill_side = models.ForeignKey(to="SideDrill", verbose_name="Gręžimo kraštinė",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.drill}"

    class Meta:
        verbose_name = 'Gręžimo eskizas'
        verbose_name_plural = 'Gręžimo eskizas'


class SketchCustom(models.Model):
    sketch_custom = models.CharField(verbose_name="Eskizas", max_length=20)
    sketch = models.ImageField(verbose_name="Eskizas", upload_to="sketch", null=True, blank=True)

    def __str__(self):
        return f"{self.sketch_custom}"

    class Meta:
        verbose_name = 'Eskizas'
        verbose_name_plural = 'Eskizas'


class MillDrawing(models.Model):
    mill_drawing = models.CharField(verbose_name="Frezavimo SCHEMA", max_length=20)
    sketch = models.ImageField(verbose_name="Eskizas", upload_to="sketch", null=True, blank=True)

    def __str__(self):
        return f"{self.mill_drawing}"

    class Meta:
        verbose_name = 'Frezavimo schema'
        verbose_name_plural = 'Frezavimo schemos'


class EdgeThickness(models.Model):
    e_thickness = models.FloatField(verbose_name="Briaunos storis mm", max_length=5)

    def __str__(self):
        return f"{self.e_thickness}"

    class Meta:
        verbose_name = 'Briaunos storis mm'
        verbose_name_plural = 'Braiunų storiai'


class TopEdgeInfo(models.Model):
    e_color = models.CharField(verbose_name="Briaunos spalva", max_length=20)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # {self.e_thickness_model}"{self.e_length}

    class Meta:
        verbose_name = 'Plokštės viršutinė briauna'
        verbose_name_plural = 'Plokščių viršutinė briauna'


class BottomEdgeInfo(models.Model):
    e_color = models.CharField(verbose_name="Briaunos spalva", max_length=20)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # "{self.e_length}

    class Meta:
        verbose_name = 'Plokštės apatinė briauna'
        verbose_name_plural = 'Plokščių apatinė briauna'


class LeftEdgeInfo(models.Model):
    e_color = models.CharField(verbose_name="Briaunos spalva", max_length=20)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # {self.e_thickness_model}"{self.e_length}

    class Meta:
        verbose_name = 'Plokštės kairė briauna'
        verbose_name_plural = 'Plokščių kairė briauna'


class RightEdgeInfo(models.Model):
    e_color = models.CharField(verbose_name="Briaunos spalva", max_length=20)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # {self.e_thickness_model}"{self.e_length}

    class Meta:
        verbose_name = 'Plokštės dešinė briauna'
        verbose_name_plural = 'Plokščių dešinė briauna'


class ProductThickness(models.Model):
    p_thickness = models.FloatField(verbose_name="Storis", max_length=5)

    def __str__(self):
        return f"{self.p_thickness} "

    class Meta:
        verbose_name = 'Plokštės storis'
        verbose_name_plural = 'Plokščių storiai'


class Product(models.Model):
    decor = models.CharField(verbose_name="Plokštės dekoras", max_length=10)
    texture = models.CharField(verbose_name="Plokštės atsparumo klasė", max_length=10)
    p_name = models.CharField(verbose_name="Plokštės pavadinimas", max_length=50)
    nsc_color = models.CharField(verbose_name="Plokštės spalvos kodas", max_length=50)
    description = models.TextField('Aprašymas', max_length=2000, default='')
    decor_pic = models.ImageField('Dekoro nuotrauka', upload_to='decors', null=True, blank=True)

    def __str__(self):
        return f"{self.decor} {self.texture} {self.p_name} {self.nsc_color}"

    class Meta:
        verbose_name = 'Plokštė'
        verbose_name_plural = 'Plokštės'


class Order(models.Model):
    order_no = models.CharField(default=uuid.uuid4().hex[:5].upper(), verbose_name="Užsakymo Numeris", max_length=10,
                                editable=False)
    date = models.DateTimeField(verbose_name="Data")
    client_name = models.ForeignKey(to=User, verbose_name="Klientas", on_delete=models.SET_NULL, null=True, blank=True)
    # client_name = models.CharField(verbose_name="Klientas", max_length=50)

    LOAN_STATUS = (
        ('p', 'Pateiktas'),
        ('a', 'Apmokėtas'),
        ('g', 'Gamyboje'),
        ('i', 'Įvykdytas'),
    )

    status = models.CharField(
        verbose_name="Būsena",
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='i',
        help_text='Statusas',
    )

    def total_length_cut(self):
        total = 0
        for line in self.lines.all():
            total += line.total_length()
        return total

    def total_width_cut(self):
        total = 0
        for line in self.lines.all():
            total += line.total_width()
        return total

    def __str__(self):
        return f"{self.order_no} {self.client_name} "

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'




class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(to="Product", verbose_name="Plokštė", on_delete=models.SET_NULL, null=True, related_name="gaminys")
    product_thickness = models.ForeignKey(to="ProductThickness", verbose_name="Storis", on_delete=models.SET_NULL,
                                          null=True)
    right_edge_info = models.ForeignKey(to="RightEdgeInfo", verbose_name="→ dešinė briauna",
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True,
                                        default=None,
                                        related_name="right_edge_info")
    left_edge_info = models.ForeignKey(to="LeftEdgeInfo", verbose_name="← kairė briauna",
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       default=None,
                                       related_name="left_edge_info")
    bottom_edge_info = models.ForeignKey(to="BottomEdgeInfo", verbose_name="↓ apatinė briauna",
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         blank=True,
                                         default=None,
                                         related_name="bottom_edge_info")
    top_edge_info = models.ForeignKey(to="TopEdgeInfo", verbose_name="↑ viršutinė briauna",
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      default=None,
                                      related_name="top_edge_info")
    mill_drawing_info = models.ForeignKey(to="MillDrawing", verbose_name="Frezavimas",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          default=None,
                                          )
    sketch_custom = models.ForeignKey(to="SketchCustom", verbose_name="Eskizas",
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      default=None,
                                      )
    sketch_drill_info = models.ForeignKey(to="DrillSketch", verbose_name="Gręžimas",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          default=None,
                                          )
    qty = models.IntegerField(verbose_name="Kiekis", )
    product_length = models.IntegerField(verbose_name="Ilgis")
    product_width = models.IntegerField(verbose_name="Plotis")

    def total_length(self):
        left_thickness = self.left_edge_info.e_thickness_model.e_thickness if self.left_edge_info else 0
        right_thickness = self.right_edge_info.e_thickness_model.e_thickness if self.right_edge_info else 0

        sum = self.product_length - left_thickness - right_thickness
        return sum

    def total_width(self):
        top_thickness = self.top_edge_info.e_thickness_model.e_thickness if self.top_edge_info else 0
        bottom_thickness = self.bottom_edge_info.e_thickness_model.e_thickness if self.bottom_edge_info else 0

        sum = self.product_width - top_thickness - bottom_thickness
        return sum


    def display_total_length(self):
        if self.product_length is not None and self.left_edge_info is not None and self.right_edge_info is not None:
            return self.product_length - self.left_edge_info.e_thickness_model.e_thickness - self.right_edge_info.e_thickness_model.e_thickness
        else:
            return None

    display_total_length.short_description = "Cut Length"

    def display_total_width(self):
        if self.product_width is not None and self.top_edge_info is not None and self.bottom_edge_info is not None:
            return self.product_width - self.top_edge_info.e_thickness_model.e_thickness - self.bottom_edge_info.e_thickness_model.e_thickness
        else:
            return None

    display_total_width.short_description = "Cut width"

    def view_sketch_image_url(self):
        if self.mill_drawing_info and self.mill_drawing_info.sketch:
            return format_html('<a href="{}" target="_blank">View Sketch Image</a>', self.mill_drawing_info.sketch.url)
        else:
            return "No sketch image available"

    view_sketch_image_url.short_description = "Sketch Image"
    view_sketch_image_url.allow_tags = True

    def sketch_image_url(self):
        if self.sketch_custom and self.sketch_custom.sketch:
            return format_html('<a href="{}" target="_blank">View Sketch Image</a>', self.sketch_custom.sketch.url)
        else:
            return "No sketch image available"

    sketch_image_url.short_description = "Sketch Image"
    sketch_image_url.allow_tags = True

    def sketch_drill_url(self):
        if self.sketch_drill_info and self.sketch_drill_info.sketch:
            return format_html('<a href="{}" target="_blank">View Sketch Image</a>', self.sketch_drill_info.sketch.url)
        else:
            return "No sketch image available"

    sketch_drill_url.short_description = "Sketch Image"
    sketch_drill_url.allow_tags = True

    def __str__(self):
        return f"{self.product} - kiekis: {self.qty}vnt -{self.total_length()}x{self.total_width()}"

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

class OrderComment(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name="Tekstas", max_length=1000)

    class Meta:
        verbose_name = 'Užsakymo komentaras'
        verbose_name_plural = 'Užsakymų komentarai'
        ordering = ['-date_created']